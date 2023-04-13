#!/usr/bin/env python3
from __future__ import annotations

from amaranth import *

from amaranth_cocotb import run, get_current_module

import cocotb
from cocotb.triggers import ClockCycles, RisingEdge
from cocotb_test.simulator import Icarus

from spi import SPI
from util import cocotb_header


async def collect_bus_data(dut, result: list[int]):
    while True:
        await RisingEdge(dut.clk)
        if dut.we.value:
            result.append(int(dut.data.value))


@cocotb.test()
async def unstable_clock(dut):
    cocotb_header(dut)
    dut.cs_n.value = 1
    dut.sck.value = 0
    dut.mosi.value = 0
    result = []
    cocotb.start_soon(collect_bus_data(dut, result))

    await ClockCycles(dut.clk, 5)
    dut.cs_n.value = 0
    await ClockCycles(dut.clk, 1)
    dut.mosi.value = 1
    await ClockCycles(dut.clk, 1)
    dut.sck.value = 1
    await ClockCycles(dut.clk, 3)
    dut.mosi.value = 0
    await ClockCycles(dut.clk, 4)
    dut.sck.value = 0
    await ClockCycles(dut.clk, 5)
    dut.sck.value = 1
    await ClockCycles(dut.clk, 6)
    dut.sck.value = 0
    await ClockCycles(dut.clk, 7)
    dut.mosi.value = 1
    await ClockCycles(dut.clk, 8)
    dut.sck.value = 1
    await ClockCycles(dut.clk, 9)
    dut.sck.value = 0
    dut.mosi.value = 0
    await ClockCycles(dut.clk, 10)
    dut.sck.value = 1
    await ClockCycles(dut.clk, 11)
    dut.sck.value = 0
    dut.mosi.value = 1
    await ClockCycles(dut.clk, 12)
    dut.sck.value = 1
    await ClockCycles(dut.clk, 13)
    dut.sck.value = 0
    dut.mosi.value = 0
    await ClockCycles(dut.clk, 14)
    dut.sck.value = 1
    await ClockCycles(dut.clk, 15)
    dut.sck.value = 0
    dut.mosi.value = 1
    await ClockCycles(dut.clk, 16)
    dut.sck.value = 1
    await ClockCycles(dut.clk, 17)
    dut.sck.value = 0
    dut.mosi.value = 0
    await ClockCycles(dut.clk, 18)
    dut.sck.value = 1
    await ClockCycles(dut.clk, 19)
    dut.sck.value = 0
    await ClockCycles(dut.clk, 20)
    dut.cs_n.value = 1
    await ClockCycles(dut.clk, 2)

    assert result == [0xAA]


def test_one_shot():
    spi = SPI()
    run(
        spi,
        get_current_module(),
        ports=spi.get_ports(),
        simulator=Icarus,
        vcd_file="test_spi.vcd",
    )
