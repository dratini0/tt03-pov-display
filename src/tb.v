`default_nettype none
`timescale 10us/10us

/*
this testbench just instantiates the module and makes some convenient wires
that can be driven / tested by the cocotb test.py
*/

module tb (
    // testbench is controlled by test.py
    input clk,
    input rst,
    input cs_n,
    input sck,
    input mosi,
    input hall_in,
    input hall_invert,
    input [1:0] divisor,

    output [7:0] leds
   );

    // this part dumps the trace to a vcd file that can be viewed with GTKWave
    initial begin
        $dumpfile ("test_pov_display_gl.fst");
        $dumpvars (0, tb);
        #1;
    end

    // wire up the inputs and outputs
    wire [7:0] inputs = {divisor, hall_invert, hall_in, mosi, sck, cs_n, clk};

    // instantiate the DUT
    dratini0_pov_display_top dratini0_pov_display_top(
        `ifdef GL_TEST
            .vccd1( 1'b1),
            .vssd1( 1'b0),
        `endif
        .io_in  (inputs),
        .io_out (leds)
        );

endmodule
