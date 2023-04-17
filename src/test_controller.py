#!/usr/bin/env python3
from amaranth import *

from amaranth_cocotb import run, get_current_module

import cocotb
from cocotb.triggers import ClockCycles, RisingEdge
from cocotb_test.simulator import Icarus

from controller import Controller
from util import cocotb_header, counter_coro, divided_clock


@cocotb.test()
async def bench(dut):
    dut.hall_in.value = 0
    dut.cs_n.value = 1
    await cocotb_header(dut)
    counter = [0]
    cocotb.start_soon(counter_coro(dut, dut.advance, counter))
    for divider in range(50, 1000, 37):
        divided_clock_task = cocotb.start_soon(divided_clock(dut, divider))
        await ClockCycles(dut.hall_in, 3)
        old_counter = counter[0]
        await RisingEdge(dut.hall_in)
        new_counter = counter[0]
        # assert 32 <= new_counter - old_counter <= 35
        divided_clock_task.cancel()


def test_controller():
    controller = Controller(depth=24)
    run(
        controller,
        get_current_module(),
        ports=controller.get_ports(),
        simulator=Icarus,
        vcd_file="test_controller.vcd",
    )
