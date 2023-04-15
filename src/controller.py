#!/usr/bin/env python3

from amaranth import *

from pulser import Pulser
from util import main


class Controller(Elaboratable):
    def __init__(self):
        self.hall_in = Signal()
        self.cs_n = Signal()

        self.advance = Signal()
        self.oe = Const(1)

        self._pulser = Pulser()

    def elaborate(self, platform):
        m = Module()
        m.submodules._pulser = self._pulser

        m.d.comb += [
            self._pulser.hall_in.eq(self.hall_in),
            self.advance.eq(self._pulser.advance),
        ]

        return m

    def get_ports(self):
        return [self.hall_in, self.addr]


if __name__ == "__main__":
    main(Controller())
