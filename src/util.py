#!/usr/bin/env python3
from amaranth import *


class OneShot(Elaboratable):
    def __init__(self):
        self.in_ = Signal()
        self.last_in = Signal()
        self.out = Signal()

    def elaborate(self, platform):
        m = Module()
        m.d.sync += self.last_in.eq(self.in_)
        m.d.comb += self.out.eq(self.in_ & ~self.last_in)
        return m
