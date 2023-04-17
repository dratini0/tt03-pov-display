#!/usr/bin/env python3
from random import randint

from amaranth import *

from amaranth_cocotb import run, get_current_module

import cocotb
from cocotb.triggers import ClockCycles, RisingEdge
from cocotb_test.simulator import Icarus

from controller import Controller
from util import cocotb_header, counter_coro, divided_clock


@cocotb.test()
async def stable_clock(dut):
    dut.hall_in.value = 0
    dut.cs_n.value = 1
    await cocotb_header(dut)
    counter = [0]
    cocotb.start_soon(counter_coro(dut, dut.advance, counter))
    dut.cs_n.value = 0
    divided_clock_task = cocotb.start_soon(divided_clock(dut, 50))
    await ClockCycles(dut.hall_in, 10)
    divided_clock_task.cancel()
    await ClockCycles(dut.clk, 25)
    dut.hall_in = 0
    dut.cs_n = 1
    await ClockCycles(dut.clk, 25)
    assert counter[0] == 0

    for divider in range(50, 1000, 37):
        divided_clock_task = cocotb.start_soon(divided_clock(dut, divider))
        await ClockCycles(dut.hall_in, 3)
        assert counter[0] % 24 == 0
        divided_clock_task.cancel()


@cocotb.test()
async def unstable_clock(dut):
    dut.hall_in.value = 0
    dut.cs_n.value = 1
    await cocotb_header(dut)
    counter = [0]
    cocotb.start_soon(counter_coro(dut, dut.advance, counter))
    dut.cs_n.value = 0
    await ClockCycles(dut.clk, 25)
    dut.cs_n.value = 1
    await ClockCycles(dut.clk, 25)
    assert counter[0] == 0

    for _ in range(10):
        for _ in range(50):
            dut.hall_in.value = 1
            await ClockCycles(dut.clk, randint(50, 500))
            dut.hall_in.value = 0
            await ClockCycles(dut.clk, randint(50, 500))
        divided_clock_task = cocotb.start_soon(divided_clock(dut, 100))
        await ClockCycles(dut.hall_in, 3)
        assert counter[0] % 24 == 0
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
