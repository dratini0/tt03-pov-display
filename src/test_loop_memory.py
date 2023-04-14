#!/usr/bin/env python3
from amaranth import *

from amaranth_cocotb import run, get_current_module

import cocotb
from cocotb.triggers import ClockCycles, RisingEdge
from cocotb_test.simulator import Icarus

from loop_memory import LoopMemory
from util import cocotb_header


@cocotb.test()
async def bench(dut):
    dut.write.value = 0
    dut.advance.value = 0
    await cocotb_header(dut)

    data = list(range(0xA0, 0xB8))
    assert len(data) == 24

    # Fill it with data in two parts
    dut.write.value = 1
    dut.advance.value = 1
    for i in data[:5]:
        dut.in_.value = i
        await RisingEdge(dut.clk)
    dut.write.value = 0
    dut.advance.value = 0

    await ClockCycles(dut.clk, 5)

    dut.write.value = 1
    dut.advance.value = 1
    for i in data[5:]:
        dut.in_.value = i
        await RisingEdge(dut.clk)
    dut.write.value = 0
    dut.advance.value = 0

    await ClockCycles(dut.clk, 5)

    # Read the whole thing back, twice over, in two parts again
    readback1 = []
    dut.advance.value = 1
    for _ in range(40):
        await RisingEdge(dut.clk)
        readback1.append(int(dut.out.value))
    dut.advance.value = 0

    await ClockCycles(dut.clk, 5)

    dut.advance.value = 1
    for _ in range(8):
        await RisingEdge(dut.clk)
        readback1.append(int(dut.out.value))
    dut.advance.value = 0

    await ClockCycles(dut.clk, 5)

    assert readback1 == data * 2


def test_loop_memory():
    loop_memory = LoopMemory(8, 24)
    run(
        loop_memory,
        get_current_module(),
        ports=loop_memory.get_ports(),
        simulator=Icarus,
        vcd_file="test_loop_memory.vcd",
    )
