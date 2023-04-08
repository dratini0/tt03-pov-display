#!/usr/bin/env python3

from amaranth import *
from amaranth.cli import main

from controller import Controller
from loop_memory import LoopMemory
from spi import SPI


class PovDisplay(Elaboratable):
    def __init__(self):
        self.cs_n = Signal()
        self.sck = Signal()
        self.mosi = Signal()
        self.hall_in = Signal()
        self.leds = Signal(8)

        self.mem = LoopMemory(width=8, depth=24)
        self.spi = SPI()

    def elaborate(self, platform):
        m = Module()
        m.submodules.mem = self.mem
        m.submodules.spi = self.spi

        m.d.comb += [
            self.spi.cs_n.eq(self.cs_n),
            self.spi.sck.eq(self.sck),
            self.spi.mosi.eq(self.mosi),
            self.mem.in_.eq(self.spi.data),
            self.mem.write.eq(self.spi.we),
            self.mem.advance.eq(self.hall_in | self.spi.we),
            self.leds.eq(self.mem.out),
        ]
        return m


if __name__ == "__main__":
    pov_display = PovDisplay()
    main(
        pov_display,
        ports=[
            pov_display.cs_n,
            pov_display.sck,
            pov_display.mosi,
            pov_display.hall_in,
            pov_display.leds,
            pov_display.leds,
        ],
    )
