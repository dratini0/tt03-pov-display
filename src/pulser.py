#!/usr/bin/env python3

from amaranth import *

from util import main, OneShot


class Pulser(Elaboratable):
    """Does its best to do 32 equally spaced pusles for ever pulse of hall_in"""

    def __init__(self, counter_width=10, shift=5):
        self.hall_in = Signal()

        self.advance = Signal()

        self._shift = shift
        self._hall_edge = OneShot()
        self._counter = Signal(counter_width, reset_less=True)
        self._last_total = Signal(counter_width, reset_less=True)
        self._comparison_signal = Signal(counter_width + shift, reset_less=True)

    def elaborate(self, platform):
        m = Module()
        m.submodules.hall_edge = self._hall_edge
        m.d.comb += self._hall_edge.in_.eq(self.hall_in)

        m.d.comb += self.advance.eq(
            self._counter >= self._comparison_signal[self._shift :]
        )
        with m.If(self._hall_edge.out):
            m.d.sync += [
                self._counter.eq(0),
                self._last_total.eq(self._counter + 1),
                self._comparison_signal.eq(0),
            ]
        with m.Else():
            m.d.sync += self._counter.eq(self._counter + 1)
            with m.If(self.advance):
                m.d.sync += self._comparison_signal.eq(
                    self._comparison_signal + self._last_total
                )

        return m

    def get_ports(self):
        return [self.hall_in, self.advance]


if __name__ == "__main__":
    main(Pulser())
