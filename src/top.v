/* Generated by Yosys 0.23 (git sha1 7ce5011c24b) */

module _pulser(rst, hall_in, divisor, advance, clk);
  reg \$auto$verilog_backend.cc:2083:dump_module$1  = 0;
  wire [9:0] \$1 ;
  wire [10:0] \$10 ;
  wire [10:0] \$11 ;
  wire [10:0] \$13 ;
  wire [11:0] \$15 ;
  wire [9:0] \$16 ;
  wire [10:0] \$18 ;
  wire [11:0] \$20 ;
  wire [10:0] \$22 ;
  wire [9:0] \$23 ;
  wire [10:0] \$25 ;
  wire [10:0] \$3 ;
  wire \$5 ;
  wire [10:0] \$7 ;
  wire [10:0] \$8 ;
  reg [7:0] _comparison_signal = 8'h00;
  reg [7:0] \_comparison_signal$next ;
  reg [9:0] _counter = 10'h000;
  reg [9:0] \_counter$next ;
  reg [7:0] _last_total = 8'h00;
  reg [7:0] \_last_total$next ;
  output advance;
  wire advance;
  input clk;
  wire clk;
  input [9:0] divisor;
  wire [9:0] divisor;
  wire hall_edge_in_;
  wire hall_edge_out;
  input hall_in;
  wire hall_in;
  input rst;
  wire rst;
  assign \$11  = _counter + 1'h1;
  assign \$18  = _comparison_signal + \$16 ;
  assign \$20  = \$18  - _last_total;
  assign \$25  = _comparison_signal + \$23 ;
  always @(posedge clk)
    _counter <= \_counter$next ;
  always @(posedge clk)
    _last_total <= \_last_total$next ;
  always @(posedge clk)
    _comparison_signal <= \_comparison_signal$next ;
  assign \$3  = _comparison_signal + \$1 ;
  assign \$5  = \$3  >= _last_total;
  assign \$8  = _counter + 1'h1;
  hall_edge hall_edge (
    .clk(clk),
    .in_(hall_edge_in_),
    .out(hall_edge_out),
    .rst(rst)
  );
  always @* begin
    if (\$auto$verilog_backend.cc:2083:dump_module$1 ) begin end
    (* full_case = 32'd1 *)
    casez (hall_edge_out)
      1'h1:
          \_counter$next  = 10'h000;
      default:
          \_counter$next  = \$8 [9:0];
    endcase
  end
  always @* begin
    if (\$auto$verilog_backend.cc:2083:dump_module$1 ) begin end
    \_last_total$next  = _last_total;
    casez (hall_edge_out)
      1'h1:
          \_last_total$next  = \$13 [7:0];
    endcase
  end
  always @* begin
    if (\$auto$verilog_backend.cc:2083:dump_module$1 ) begin end
    (* full_case = 32'd1 *)
    casez (hall_edge_out)
      1'h1:
          \_comparison_signal$next  = 8'h00;
      default:
          (* full_case = 32'd1 *)
          casez (advance)
            1'h1:
                \_comparison_signal$next  = \$20 [7:0];
            default:
                \_comparison_signal$next  = \$25 [7:0];
          endcase
    endcase
  end
  assign \$7  = \$8 ;
  assign \$10  = \$13 ;
  assign \$15  = \$20 ;
  assign \$22  = \$25 ;
  assign advance = \$5 ;
  assign hall_edge_in_ = hall_in;
  assign \$1  = { 2'h0, divisor[9:2] };
  assign \$13  = { 2'h0, \$11 [10:2] };
  assign \$16  = { 2'h0, divisor[9:2] };
  assign \$23  = { 2'h0, divisor[9:2] };
endmodule

module controller(rst, hall_in, cs_n, advance, divisor, oe, clk);
  reg \$auto$verilog_backend.cc:2083:dump_module$2  = 0;
  wire \$1 ;
  wire \$11 ;
  wire [5:0] \$13 ;
  wire [5:0] \$14 ;
  wire \$3 ;
  wire \$5 ;
  wire \$7 ;
  wire \$9 ;
  reg [4:0] _count = 5'h00;
  reg [4:0] \_count$next ;
  wire _pulser_advance;
  wire [9:0] _pulser_divisor;
  wire _pulser_hall_in;
  reg _state = 1'h0;
  reg \_state$next ;
  output advance;
  wire advance;
  input clk;
  wire clk;
  input cs_n;
  wire cs_n;
  input [9:0] divisor;
  wire [9:0] divisor;
  wire hall_edge_in_;
  wire hall_edge_out;
  input hall_in;
  wire hall_in;
  output oe;
  wire oe;
  input rst;
  wire rst;
  assign \$9  = _count >= 5'h18;
  assign \$11  = oe & _pulser_advance;
  assign \$14  = _count + 1'h1;
  always @(posedge clk)
    _state <= \_state$next ;
  always @(posedge clk)
    _count <= \_count$next ;
  assign \$1  = _pulser_advance & oe;
  assign \$3  = cs_n & _state;
  assign \$5  = _count < 5'h18;
  assign \$7  = \$3  & \$5 ;
  _pulser _pulser (
    .advance(_pulser_advance),
    .clk(clk),
    .divisor(_pulser_divisor),
    .hall_in(_pulser_hall_in),
    .rst(rst)
  );
  \hall_edge$1  hall_edge (
    .clk(clk),
    .in_(hall_edge_in_),
    .out(hall_edge_out),
    .rst(rst)
  );
  always @* begin
    if (\$auto$verilog_backend.cc:2083:dump_module$2 ) begin end
    \_state$next  = _state;
    (* full_case = 32'd1 *)
    casez (cs_n)
      1'h1:
          casez (hall_edge_out)
            1'h1:
                \_state$next  = 1'h1;
          endcase
      default:
          \_state$next  = 1'h0;
    endcase
  end
  always @* begin
    if (\$auto$verilog_backend.cc:2083:dump_module$2 ) begin end
    \_count$next  = _count;
    (* full_case = 32'd1 *)
    casez (cs_n)
      1'h1:
          casez (hall_edge_out)
            1'h1:
                casez (\$9 )
                  1'h1:
                      \_count$next  = 5'h00;
                endcase
          endcase
      default:
          \_count$next  = 5'h18;
    endcase
    casez (\$11 )
      1'h1:
          \_count$next  = \$14 [4:0];
    endcase
  end
  assign \$13  = \$14 ;
  assign oe = \$7 ;
  assign hall_edge_in_ = hall_in;
  assign advance = \$1 ;
  assign _pulser_divisor = divisor;
  assign _pulser_hall_in = hall_in;
endmodule

module display(rst, cs_n, sck, mosi, hall_in, hall_invert, divisor, leds, clk);
  reg \$auto$verilog_backend.cc:2083:dump_module$3  = 0;
  wire \$1 ;
  wire \$3 ;
  input clk;
  wire clk;
  wire controller_advance;
  wire controller_cs_n;
  reg [9:0] controller_divisor;
  wire controller_hall_in;
  wire controller_oe;
  input cs_n;
  wire cs_n;
  input [1:0] divisor;
  wire [1:0] divisor;
  input hall_in;
  wire hall_in;
  input hall_invert;
  wire hall_invert;
  output [7:0] leds;
  reg [7:0] leds;
  wire mem_advance;
  wire [7:0] mem_in_;
  wire [7:0] mem_out;
  wire mem_write;
  input mosi;
  wire mosi;
  input rst;
  wire rst;
  input sck;
  wire sck;
  wire spi_cs_n;
  wire [7:0] spi_data;
  wire spi_mosi;
  wire spi_sck;
  wire spi_we;
  assign \$1  = hall_in ^ hall_invert;
  assign \$3  = controller_advance | spi_we;
  controller controller (
    .advance(controller_advance),
    .clk(clk),
    .cs_n(controller_cs_n),
    .divisor(controller_divisor),
    .hall_in(controller_hall_in),
    .oe(controller_oe),
    .rst(rst)
  );
  mem mem (
    .advance(mem_advance),
    .clk(clk),
    .in_(mem_in_),
    .out(mem_out),
    .rst(rst),
    .write(mem_write)
  );
  spi spi (
    .clk(clk),
    .cs_n(spi_cs_n),
    .data(spi_data),
    .mosi(spi_mosi),
    .rst(rst),
    .sck(spi_sck),
    .we(spi_we)
  );
  always @* begin
    if (\$auto$verilog_backend.cc:2083:dump_module$3 ) begin end
    (* full_case = 32'd1 *)
    casez (divisor)
      2'h0:
          controller_divisor = 10'h020;
      2'h1:
          controller_divisor = 10'h030;
      2'h2:
          controller_divisor = 10'h040;
      2'h3:
          controller_divisor = 10'h060;
    endcase
  end
  always @* begin
    if (\$auto$verilog_backend.cc:2083:dump_module$3 ) begin end
    (* full_case = 32'd1 *)
    casez (controller_oe)
      1'h1:
          leds = mem_out;
      default:
          leds = 8'h00;
    endcase
  end
  assign mem_advance = \$3 ;
  assign mem_write = spi_we;
  assign mem_in_ = spi_data;
  assign controller_cs_n = cs_n;
  assign controller_hall_in = \$1 ;
  assign spi_mosi = mosi;
  assign spi_sck = sck;
  assign spi_cs_n = cs_n;
endmodule

module dratini0_pov_display_top(io_out, io_in);
  wire display_clk;
  wire display_cs_n;
  wire [1:0] display_divisor;
  wire display_hall_in;
  wire display_hall_invert;
  wire [7:0] display_leds;
  wire display_mosi;
  wire display_rst;
  wire display_sck;
  input [7:0] io_in;
  wire [7:0] io_in;
  output [7:0] io_out;
  wire [7:0] io_out;
  display display (
    .clk(display_clk),
    .cs_n(display_cs_n),
    .divisor(display_divisor),
    .hall_in(display_hall_in),
    .hall_invert(display_hall_invert),
    .leds(display_leds),
    .mosi(display_mosi),
    .rst(1'h0),
    .sck(display_sck)
  );
  assign io_out = display_leds;
  assign display_divisor = io_in[7:6];
  assign display_hall_invert = io_in[5];
  assign display_hall_in = io_in[4];
  assign display_mosi = io_in[3];
  assign display_sck = io_in[2];
  assign display_cs_n = io_in[1];
  assign display_rst = 1'h0;
  assign display_clk = io_in[0];
endmodule

module hall_edge(rst, in_, out, clk);
  wire \$1 ;
  wire \$3 ;
  input clk;
  wire clk;
  input in_;
  wire in_;
  reg last_in = 1'h0;
  wire \last_in$next ;
  output out;
  wire out;
  input rst;
  wire rst;
  assign \$1  = ~ last_in;
  assign \$3  = in_ & \$1 ;
  always @(posedge clk)
    last_in <= \last_in$next ;
  assign out = \$3 ;
  assign \last_in$next  = in_;
endmodule

module \hall_edge$1 (rst, in_, out, clk);
  wire \$1 ;
  wire \$3 ;
  input clk;
  wire clk;
  input in_;
  wire in_;
  reg last_in = 1'h0;
  wire \last_in$next ;
  output out;
  wire out;
  input rst;
  wire rst;
  assign \$1  = ~ last_in;
  assign \$3  = in_ & \$1 ;
  always @(posedge clk)
    last_in <= \last_in$next ;
  assign out = \$3 ;
  assign \last_in$next  = in_;
endmodule

module mem(rst, in_, write, advance, out, clk);
  reg \$auto$verilog_backend.cc:2083:dump_module$4  = 0;
  reg [191:0] _state = 192'h000000000000000000000000000000000000000000000000;
  reg [191:0] \_state$next ;
  input advance;
  wire advance;
  input clk;
  wire clk;
  input [7:0] in_;
  wire [7:0] in_;
  output [7:0] out;
  wire [7:0] out;
  input rst;
  wire rst;
  input write;
  wire write;
  always @(posedge clk)
    _state <= \_state$next ;
  always @* begin
    if (\$auto$verilog_backend.cc:2083:dump_module$4 ) begin end
    \_state$next  = _state;
    casez (advance)
      1'h1:
        begin
          \_state$next [191:8] = _state[183:0];
          (* full_case = 32'd1 *)
          casez (write)
            1'h1:
                \_state$next [7:0] = in_;
            default:
                \_state$next [7:0] = out;
          endcase
        end
    endcase
  end
  assign out = _state[191:184];
endmodule

module sck_edge(rst, in_, out, clk);
  wire \$1 ;
  wire \$3 ;
  input clk;
  wire clk;
  input in_;
  wire in_;
  reg last_in = 1'h0;
  wire \last_in$next ;
  output out;
  wire out;
  input rst;
  wire rst;
  assign \$1  = ~ last_in;
  assign \$3  = in_ & \$1 ;
  always @(posedge clk)
    last_in <= \last_in$next ;
  assign out = \$3 ;
  assign \last_in$next  = in_;
endmodule

module spi(rst, cs_n, sck, mosi, data, we, clk);
  reg \$auto$verilog_backend.cc:2083:dump_module$5  = 0;
  wire \$1 ;
  wire \$12 ;
  wire \$14 ;
  wire [9:0] \$16 ;
  wire [9:0] \$17 ;
  wire \$19 ;
  wire \$21 ;
  wire \$23 ;
  wire \$25 ;
  wire \$3 ;
  wire [3:0] \$5 ;
  wire [3:0] \$6 ;
  wire \$8 ;
  wire \$9 ;
  reg [2:0] _bit_index = 3'h0;
  reg [2:0] \_bit_index$next ;
  input clk;
  wire clk;
  input cs_n;
  wire cs_n;
  output [7:0] data;
  reg [7:0] data = 8'h00;
  reg [7:0] \data$next ;
  input mosi;
  wire mosi;
  input rst;
  wire rst;
  input sck;
  wire sck;
  wire sck_edge_in_;
  wire sck_edge_out;
  output we;
  reg we = 1'h0;
  wire \we$next ;
  assign \$9  = ~ cs_n;
  assign \$12  = ~ cs_n;
  assign \$14  = \$12  & sck_edge_out;
  assign \$17  = { data, 1'h0 } + mosi;
  assign \$1  = ~ cs_n;
  assign \$19  = ~ cs_n;
  assign \$21  = \$19  & sck_edge_out;
  assign \$23  = _bit_index == 3'h7;
  assign \$25  = \$21  & \$23 ;
  always @(posedge clk)
    _bit_index <= \_bit_index$next ;
  always @(posedge clk)
    data <= \data$next ;
  always @(posedge clk)
    we <= \we$next ;
  assign \$3  = \$1  & sck_edge_out;
  assign \$6  = _bit_index + 1'h1;
  sck_edge sck_edge (
    .clk(clk),
    .in_(sck_edge_in_),
    .out(sck_edge_out),
    .rst(rst)
  );
  always @* begin
    if (\$auto$verilog_backend.cc:2083:dump_module$5 ) begin end
    \_bit_index$next  = _bit_index;
    casez (\$3 )
      1'h1:
          \_bit_index$next  = \$6 [2:0];
    endcase
    casez (\$8 )
      1'h1:
          \_bit_index$next  = 3'h0;
    endcase
  end
  always @* begin
    if (\$auto$verilog_backend.cc:2083:dump_module$5 ) begin end
    \data$next  = data;
    casez (\$14 )
      1'h1:
          \data$next  = \$17 [7:0];
    endcase
  end
  assign \$5  = \$6 ;
  assign \$16  = \$17 ;
  assign \we$next  = \$25 ;
  assign sck_edge_in_ = sck;
  assign \$8  = cs_n;
endmodule

