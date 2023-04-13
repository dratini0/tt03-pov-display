from amaranth.sim import Simulator

from util import OneShot

def test_one_shot_amaranth():
    dut = OneShot()
    def bench():
        for _ in range(10):
            yield dut.in_.eq(0)
            for _ in range(10):
                yield
                assert not (yield dut.out)
            yield dut.in_.eq(1)
            yield
            assert (yield dut.out)
            for _ in range(10):
                yield
                assert not (yield dut.out)

    sim = Simulator(dut)
    sim.add_clock(1/12500)
    sim.add_sync_process(bench)
    with sim.write_vcd("test_one_shot_amaranth.vcd"):
        sim.run()
