#!/usr/bin/env python3

from amaranth import *
from amaranth.back import verilog

from pov_display import PovDisplay


class PovDisplayTop(Elaboratable):
    """The top level, responsible for pinout definition"""

    def __init__(self):
        self.io_in = Signal(8)
        self.io_out = Signal(8)
        self.display = PovDisplay(width=8, depth=32)

    def elaborate(self, platform):
        m = Module()

        clk_in = self.io_in[0]
        cs_n = self.io_in[1]
        sck = self.io_in[2]
        mosi = self.io_in[3]
        hall_in = self.io_in[4]
        hall_invert = self.io_in[5]
        divisor = self.io_in[6:8]

        # Set up clock domain from io_in[0]
        cd_sync = ClockDomain("sync")
        m.d.comb += cd_sync.clk.eq(clk_in)
        m.d.comb += cd_sync.rst.eq(0)
        m.domains += cd_sync

        # Tie POV display to pins
        m.submodules.display = self.display
        m.d.comb += [
            self.display.cs_n.eq(cs_n),
            self.display.sck.eq(sck),
            self.display.mosi.eq(mosi),
            self.display.hall_in.eq(hall_in),
            self.display.hall_invert.eq(hall_invert),
            self.display.divisor.eq(divisor),
            self.io_out.eq(self.display.leds),
        ]

        return m

    def get_ports(self):
        return [self.io_in, self.io_out]


if __name__ == "__main__":
    top = PovDisplayTop()
    print(
        verilog.convert(
            top,
            ports=top.get_ports(),
            name="dratini0_pov_display_top",
            emit_src=False,
            strip_internal_attrs=True,
        )
    )
