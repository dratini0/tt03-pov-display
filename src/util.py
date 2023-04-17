#!/usr/bin/env python3
from amaranth import *
import amaranth.cli

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, RisingEdge


class OneShot(Elaboratable):
    def __init__(self, reset_less=True):
        self.in_ = Signal()
        self.last_in = Signal(reset_less=reset_less)
        self.out = Signal()

    def elaborate(self, platform):
        m = Module()
        m.d.sync += self.last_in.eq(self.in_)
        m.d.comb += self.out.eq(self.in_ & ~self.last_in)
        return m

    def get_ports(self):
        return [self.in_, self.out]


def main(fragment):
    amaranth.cli.main(fragment, ports=fragment.get_ports())


async def cocotb_header(dut):
    cocotb.start_soon(Clock(dut.clk, 80, units="us").start())
    dut.rst.value = 1
    await ClockCycles(dut.clk, 5)
    dut.rst.value = 0
    await ClockCycles(dut.clk, 5)


async def divided_clock(dut, factor):
    while True:
        dut.hall_in.value = 1
        await ClockCycles(dut.clk, factor // 2)
        dut.hall_in.value = 0
        await ClockCycles(dut.clk, factor - factor // 2)


async def counter_coro(dut, signal, counter):
    while True:
        await RisingEdge(dut.clk)
        counter[0] += int(signal.value)
