#!/usr/bin/env python3
from amaranth import *

from amaranth_cocotb import run, get_current_module

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer
from cocotb_test.simulator import Icarus

from util import OneShot


@cocotb.test()
async def bench(dut):
    dut.rst.value = 0
    cocotb.start_soon(Clock(dut.clk, 80, units="us").start())
    for _ in range(10):
        dut.in_.value = 0
        for _ in range(10):
            await RisingEdge(dut.clk)
            assert not dut.out.value
        dut.in_.value = 1
        await RisingEdge(dut.clk)
        assert dut.out.value
        for _ in range(10):
            await RisingEdge(dut.clk)
            assert not dut.out.value


def test_one_shot():
    one_shot = OneShot()
    run(
        one_shot,
        get_current_module(),
        ports=one_shot.get_ports(),
        simulator=Icarus,
        vcd_file="test_one_shot.vcd",
    )
