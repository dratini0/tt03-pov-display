#!/usr/bin/env python3

from amaranth import *

from util import main


class LoopMemory(Elaboratable):
    def __init__(self, width, depth):
        self.in_ = Signal(width)
        self.out = Signal(width)
        self.advance = Signal()
        self.write = Signal()
        self._state = Signal(width * depth, reset_less=True)
        self._width = width

    def elaborate(self, platform):
        m = Module()
        m.d.comb += self.out.eq(self._state[-self._width :])
        with m.If(self.advance):
            m.d.sync += self._state[self._width :].eq(self._state[: -self._width])
            with m.If(self.write):
                m.d.sync += self._state[: self._width].eq(self.in_)
            with m.Else():
                m.d.sync += self._state[: self._width].eq(self.out)

        return m

    def get_ports(self):
        return [
            self.in_,
            self.out,
            self.advance,
            self.write,
        ]


if __name__ == "__main__":
    main(LoopMemory(8, 24))
