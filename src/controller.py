#!/usr/bin/env python3

from amaranth import *

from pulser import Pulser
from util import main, OneShot


class Controller(Elaboratable):
    def __init__(self, depth):
        self.hall_in = Signal()
        self.cs_n = Signal()

        self.advance = Signal()
        self.oe = Signal()

        self._pulser = Pulser(divisor=depth.bit_length())
        self._hall_edge = OneShot()
        self._state = Signal(1, reset_less=True)
        self._count = Signal(range(0, depth + 1), reset_less=True)

        self._depth = depth

    def elaborate(self, platform):
        m = Module()

        m.submodules._pulser = self._pulser
        m.d.comb += [
            self._pulser.hall_in.eq(self.hall_in),
            self.advance.eq(self._pulser.advance),
        ]

        m.submodules.hall_edge = self._hall_edge
        m.d.comb += self._hall_edge.in_.eq(self.hall_in)

        m.d.comb += [
            self.oe.eq(self.cs_n & self._state & (self._count < self._depth)),
            self.advance.eq(self._pulser.advance & self.oe),
        ]

        with m.If(self.cs_n):
            # Not selected (we control memory)
            with m.If(self._hall_edge.out):
                m.d.sync += self._state.eq(1)
                with m.If(self._count >= self._depth):
                    m.d.sync += self._count.eq(0)
        with m.Else():
            # Selected (host controls memory)
            m.d.sync += [
                self._state.eq(0),
                self._count.eq(self._depth),
            ]

        with m.If(self.oe & self._pulser.advance):
            m.d.sync += self._count.eq(self._count + 1)

        return m

    def get_ports(self):
        return [self.hall_in, self.cs_n, self.advance, self.oe]


if __name__ == "__main__":
    main(Controller(24))
