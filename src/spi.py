#!/usr/bin/env python3

from amaranth import *
from amaranth.cli import main

from util import OneShot


class SPI(Elaboratable):
    def __init__(self):
        self.cs_n = Signal()
        self.sck = Signal()
        self.mosi = Signal()

        self.addr = Signal(8)
        self.data = Signal(8)
        self.we = Signal()

        self.bit_index = Signal(3)

        self.sck_edge = OneShot()

    def elaborate(self, platform):
        cs = ~self.cs_n

        m = Module()

        m.submodules.sck_edge = self.sck_edge
        m.d.comb += self.sck_edge.in_.eq(self.sck)

        with m.If(cs & self.sck_edge.out):
            m.d.sync += [
                self.bit_index.eq(self.bit_index + 1),
                self.data.eq(self.data.shift_left(1) + self.mosi),
            ]
            with m.If(self.bit_index == 7):
                m.d.sync += self.addr.eq(self.addr + 1)
        m.d.comb += self.we.eq(cs & self.sck_edge.out & (self.bit_index == 7))

        return m


if __name__ == "__main__":
    spi = SPI()
    main(spi, ports=[spi.cs_n, spi.sck, spi.mosi, spi.data, spi.we])
