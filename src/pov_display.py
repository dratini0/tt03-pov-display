#!/usr/bin/env python3

from amaranth import *

from controller import Controller
from loop_memory import LoopMemory
from spi import SPI
from util import main


class PovDisplay(Elaboratable):
    def __init__(self):
        self.cs_n = Signal()
        self.sck = Signal()
        self.mosi = Signal()
        self.hall_in = Signal()
        self.leds = Signal(8)

        self._mem = LoopMemory(width=8, depth=24)
        self._spi = SPI()

    def elaborate(self, platform):
        m = Module()
        m.submodules.mem = self._mem
        m.submodules.spi = self._spi

        m.d.comb += [
            self._spi.cs_n.eq(self.cs_n),
            self._spi.sck.eq(self.sck),
            self._spi.mosi.eq(self.mosi),
            self._mem.in_.eq(self._spi.data),
            self._mem.write.eq(self._spi.we),
            self._mem.advance.eq(self.hall_in | self._spi.we),
            self.leds.eq(self._mem.out),
        ]
        return m

    def get_ports(self):
        return [
            self.cs_n,
            self.sck,
            self.mosi,
            self.hall_in,
            self.leds,
            self.leds,
        ]


if __name__ == "__main__":
    main(PovDisplay())
