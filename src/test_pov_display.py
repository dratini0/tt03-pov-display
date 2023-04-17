#!/usr/bin/env python3
from random import randint

from amaranth import *

from amaranth_cocotb import run, get_current_module

import cocotb
from cocotb.triggers import ClockCycles, RisingEdge
from cocotb_test.simulator import Icarus

from pov_display import PovDisplay
from util import (
    bytes_to_bitstream,
    cocotb_header,
    divided_clock,
    send_bitstream,
)


@cocotb.test()
async def stable_clock(dut):
    dut.hall_in.value = 0
    dut.cs_n.value = 1
    dut.sck.value = 0
    dut.mosi.value = 0
    await cocotb_header(dut)
    divided_clock_task = cocotb.start_soon(divided_clock(dut, 50))
    await send_bitstream(dut, bytes_to_bitstream(range(1, 25)))
    await RisingEdge(dut.hall_in)
    divided_clock_task.cancel()

    for divider in range(50, 1000, 37):
        divided_clock_task = cocotb.start_soon(divided_clock(dut, divider))
        await ClockCycles(dut.hall_in, 3)
        divided_clock_task.cancel()


def test_pov_display():
    pov_display = PovDisplay(width=8, depth=24)
    run(
        pov_display,
        get_current_module(),
        ports=pov_display.get_ports(),
        simulator=Icarus,
        vcd_file="test_pov_display.vcd",
    )
