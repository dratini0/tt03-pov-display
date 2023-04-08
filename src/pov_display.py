#!/usr/bin/env python3

from amaranth import *
from amaranth.back import verilog

class EdgeDetect(Elaboratable):
    def __init__(self):
        self.in_ = Signal()
        self.last_in = Signal()
        self.out = Signal()

    def elaborate(self, platform):
        m = Module()
        m.d.sync += self.last_in.eq(self.in_)
        m.d.comb += self.out.eq(self.in_ & ~ self.last_in)
        return m


class SPI(Elaboratable):
    def __init__(self):
        self.cs_n = Signal()
        self.sck = Signal()
        self.mosi = Signal()

        self.addr = Signal(8)
        self.data = Signal(8)
        self.we = Signal()

        self.bit_index = Signal(3)

        self.sck_edge = EdgeDetect()

    def elaborate(self, platform):
        cs = ~self.cs_n

        m = Module()

        m.submodules.sck_edge = self.sck_edge
        m.d.comb += self.sck_edge.in_.eq(self.sck)

        with m.If(cs & self.sck_edge.out):
            m.d.sync += [
                self.bit_index.eq(self.bit_index + 1),
                self.data.eq(self.data.shift_left(1) + self.mosi)
            ]
            with m.If(self.bit_index == 7):
                m.d.sync += self.addr.eq(self.addr + 1)
        m.d.comb += self.we.eq(cs & self.sck_edge.out & (self.bit_index == 7))

        return m


class Controller(Elaboratable):
    def __init__(self):
        self.hall_in = Signal()
        self.addr = Signal(8)

    def elaborate(self, platform):
        m = Module()
        m.d.sync += self.addr.eq(self.addr + 1)
        return m


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
        m.d.comb += self.out.eq(self._state[:self._width])
        with m.If(self.advance):
            m.d.sync += self._state[self._width:].eq(self._state[:-self._width])
            with m.If(self.write):
                m.d.sync += self._state[:self._width].eq(self.in_)
            with m.Else():
                m.d.sync += self._state[:self._width].eq(self._state[-self._width:])

        return m


class PovDisplay(Elaboratable):
    def __init__(self):
        self.cs_n = Signal()
        self.sck = Signal()
        self.mosi = Signal()
        self.hall_in = Signal()
        self.leds = Signal(8)

        self.mem = LoopMemory(width=8, depth=24)
        self.spi = SPI()

    def elaborate(self, platform):
        m = Module()
        m.submodules.mem = self.mem
        m.submodules.spi = self.spi

        m.d.comb += [
            self.spi.cs_n.eq(self.cs_n),
            self.spi.sck.eq(self.sck),
            self.spi.mosi.eq(self.mosi),

            self.mem.in_.eq(self.spi.data),
            self.mem.write.eq(self.spi.we),
            self.mem.advance.eq(self.hall_in | self.spi.we),
            self.leds.eq(self.mem.out),

        ]
        return m


class PovDisplayWrapper(Elaboratable):
    """The top level, responsible for pinout definition"""
    def __init__(self):
        self.io_in = Signal(8)
        self.io_out = Signal(8)
        self.display = PovDisplay()

    def elaborate(self, platform):
        m = Module()

        clk_in = self.io_in[0]
        rst_in = self.io_in[1]
        cs_n = self.io_in[2]
        sck = self.io_in[3]
        mosi = self.io_in[4]
        hall_in = self.io_in[5]


        # Set up clock domain from io_in[0] and reset from io_in[1].
        cd_sync = ClockDomain("sync")
        m.d.comb += cd_sync.clk.eq(clk_in)
        m.d.comb += cd_sync.rst.eq(rst_in)
        m.domains += cd_sync

        # Tie POV display to pins
        m.submodules.display = self.display
        m.d.comb += [
            self.display.cs_n.eq(cs_n),
            self.display.sck.eq(sck),
            self.display.mosi.eq(mosi),
            self.display.hall_in.eq(hall_in),
            self.io_out.eq(self.display.leds),
        ]

        return m


if __name__ == "__main__":
    top = PovDisplayWrapper()
    print(
        verilog.convert(
            top,
            ports=[top.io_in, top.io_out],
            name="dratini0_pov_display_top",
            emit_src=False,
            strip_internal_attrs=True,
        )
    )
