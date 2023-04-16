#!/usr/bin/env python3
from amaranth import *

from amaranth_cocotb import run, get_current_module

import cocotb
from cocotb.triggers import ClockCycles, RisingEdge, Timer
from cocotb_test.simulator import Icarus

from pulser import Pulser
from util import cocotb_header


async def divided_clock(dut, factor):
    while True:
        dut.hall_in.value = 1
        await RisingEdge(dut.clk)
        dut.hall_in.value = 0
        await ClockCycles(dut.clk, factor - 1)


async def counter_coro(dut, signal, counter):
    while True:
        await RisingEdge(dut.clk)
        counter[0] += int(signal.value)


@cocotb.test()
async def bench(dut):
    dut.hall_in.value = 0
    await cocotb_header(dut)
    counter = [0]
    cocotb.start_soon(counter_coro(dut, dut.advance, counter))
    for divider in range(50, 1000, 37):
        divided_clock_task = cocotb.start_soon(divided_clock(dut, divider))
        await ClockCycles(dut.hall_in, 3)
        old_counter = counter[0]
        await RisingEdge(dut.hall_in)
        new_counter = counter[0]
        assert 32 <= new_counter - old_counter <= 35
        divided_clock_task.cancel()


def test_pulser():
    pulser = Pulser()
    run(
        pulser,
        get_current_module(),
        ports=pulser.get_ports(),
        simulator=Icarus,
        vcd_file="test_pulser.vcd",
    )
