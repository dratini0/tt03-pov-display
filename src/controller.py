#!/usr/bin/env python3

from amaranth import *
from amaranth.cli import main


class Controller(Elaboratable):
    def __init__(self):
        self.hall_in = Signal()
        self.addr = Signal(8)

    def elaborate(self, platform):
        m = Module()
        m.d.sync += self.addr.eq(self.addr + 1)
        return m


if __name__ == "__main__":
    controller = Controller()
    main(controller, ports=[controller.hall_in, controller.addr])
