#!/usr/bin/env python3
from random import choice, randint

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
    dut.divisor.value = 48
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

    for divisor in [48, 64, 96, 128]:
        dut.divisor.value = divisor
        for period in range(50, 1000, 37):
            if period < divisor + 10:
                continue
            divided_clock_task = cocotb.start_soon(divided_clock(dut, period))
            await ClockCycles(dut.hall_in, 3)
            assert counter[0] % 32 == 0
            divided_clock_task.cancel()


@cocotb.test()
async def unstable_clock(dut):
    dut.hall_in.value = 0
    dut.cs_n.value = 1
    dut.divisor.value = 48
    await cocotb_header(dut)
    counter = [0]
    cocotb.start_soon(counter_coro(dut, dut.advance, counter))
    dut.cs_n.value = 0
    await ClockCycles(dut.clk, 25)
    dut.cs_n.value = 1
    await ClockCycles(dut.clk, 25)
    assert counter[0] == 0

    for _ in range(10):
        for _ in range(20):
            dut.divisor.value = choice([48, 64, 96, 128])
            dut.hall_in.value = 1
            await ClockCycles(dut.clk, randint(50, 500))
            dut.hall_in.value = 0
            await ClockCycles(dut.clk, randint(50, 500))
        divided_clock_task = cocotb.start_soon(divided_clock(dut, 100))
        await ClockCycles(dut.hall_in, 3)
        assert counter[0] % 32 == 0
        divided_clock_task.cancel()


def test_controller():
    controller = Controller(depth=32)
    run(
        controller,
        get_current_module(),
        ports=controller.get_ports(),
        simulator=Icarus,
        vcd_file="test_controller.vcd",
    )
