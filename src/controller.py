#!/usr/bin/env python3

from amaranth import *

from util import main


class Controller(Elaboratable):
    def __init__(self):
        self.hall_in = Signal()
        self.addr = Signal(8)

    def elaborate(self, platform):
        m = Module()
        m.d.sync += self.addr.eq(self.addr + 1)
        return m

    def get_ports(self):
        return [self.hall_in, self.addr]


if __name__ == "__main__":
    main(Controller())
