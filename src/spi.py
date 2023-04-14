#!/usr/bin/env python3

from amaranth import *
from amaranth.cli import main

from util import main, OneShot


class SPI(Elaboratable):
    def __init__(self):
        self.cs_n = Signal()
        self.sck = Signal()
        self.mosi = Signal()

        self.data = Signal(8)
        self.we = Signal()

        self._bit_index = Signal(3, reset_less=True)

        self._sck_edge = OneShot()
        self._cs_edge = OneShot()

    def elaborate(self, platform):
        cs = ~self.cs_n

        m = Module()

        m.submodules.sck_edge = self._sck_edge
        m.d.comb += self._sck_edge.in_.eq(self.sck)

        m.submodules.cs_edge = self._cs_edge
        m.d.comb += self._cs_edge.in_.eq(cs)

        with m.If(cs & self._sck_edge.out):
            m.d.sync += [
                self._bit_index.eq(self._bit_index + 1),
                self.data.eq(self.data.shift_left(1) + self.mosi),
            ]
        m.d.sync += self.we.eq(cs & self._sck_edge.out & (self._bit_index == 7))

        with m.If(self._cs_edge.out):
            m.d.sync += self._bit_index.eq(0)

        return m

    def get_ports(self):
        return [self.cs_n, self.sck, self.mosi, self.data, self.we]


if __name__ == "__main__":
    main(SPI())
