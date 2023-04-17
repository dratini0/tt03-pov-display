#!/usr/bin/env python3
from amaranth import *

from amaranth_cocotb import run, get_current_module

import cocotb
from cocotb.triggers import ClockCycles, RisingEdge
from cocotb_test.simulator import Icarus

from pulser import Pulser
from util import cocotb_header, counter_coro, divided_clock


ROUNDING = 0


@cocotb.test()
async def bench(dut):
    dut.hall_in.value = 0
    dut.divisor.value = 48
    await cocotb_header(dut)
    counter = [0]
    cocotb.start_soon(counter_coro(dut, dut.advance, counter))
    for divisor in [48, 64, 96, 128]:
        dut.divisor.value = divisor
        for period in range(50, 1000, 37):
            if period < divisor + 10:
                continue
            divided_clock_task = cocotb.start_soon(divided_clock(dut, period))
            await ClockCycles(dut.hall_in, 3)
            old_counter = counter[0]
            await RisingEdge(dut.hall_in)
            new_counter = counter[0]
            assert divisor <= new_counter - old_counter < divisor + (1 << ROUNDING)
            divided_clock_task.cancel()


def test_pulser():
    pulser = Pulser(rounding=ROUNDING)
    run(
        pulser,
        get_current_module(),
        ports=pulser.get_ports(),
        simulator=Icarus,
        vcd_file="test_pulser.vcd",
    )
