/* Generated by Yosys 0.23 (git sha1 7ce5011c24b) */

module display(rst, cs_n, sck, mosi, hall_in, leds, clk);
  wire \$1 ;
  input clk;
  wire clk;
  input cs_n;
  wire cs_n;
  input hall_in;
  wire hall_in;
  output [7:0] leds;
  wire [7:0] leds;
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
  assign \$1  = hall_in | spi_we;
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
  assign leds = mem_out;
  assign mem_advance = \$1 ;
  assign mem_write = spi_we;
  assign mem_in_ = spi_data;
  assign spi_mosi = mosi;
  assign spi_sck = sck;
  assign spi_cs_n = cs_n;
endmodule

module dratini0_pov_display_top(io_out, io_in);
  wire display_clk;
  wire display_cs_n;
  wire display_hall_in;
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
    .hall_in(display_hall_in),
    .leds(display_leds),
    .mosi(display_mosi),
    .rst(display_rst),
    .sck(display_sck)
  );
  assign io_out = display_leds;
  assign display_hall_in = io_in[5];
  assign display_mosi = io_in[4];
  assign display_sck = io_in[3];
  assign display_cs_n = io_in[2];
  assign display_rst = io_in[1];
  assign display_clk = io_in[0];
endmodule

module mem(rst, in_, write, advance, out, clk);
  reg \$auto$verilog_backend.cc:2083:dump_module$1  = 0;
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
    if (\$auto$verilog_backend.cc:2083:dump_module$1 ) begin end
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
                \_state$next [7:0] = _state[191:184];
          endcase
        end
    endcase
  end
  assign out = _state[7:0];
endmodule

module sck_edge(rst, in_, out, clk);
  reg \$auto$verilog_backend.cc:2083:dump_module$2  = 0;
  wire \$1 ;
  wire \$3 ;
  input clk;
  wire clk;
  input in_;
  wire in_;
  reg last_in = 1'h0;
  reg \last_in$next ;
  output out;
  wire out;
  input rst;
  wire rst;
  assign \$1  = ~ last_in;
  assign \$3  = in_ & \$1 ;
  always @(posedge clk)
    last_in <= \last_in$next ;
  always @* begin
    if (\$auto$verilog_backend.cc:2083:dump_module$2 ) begin end
    \last_in$next  = in_;
    casez (rst)
      1'h1:
          \last_in$next  = 1'h0;
    endcase
  end
  assign out = \$3 ;
endmodule

module spi(rst, cs_n, sck, mosi, data, we, clk);
  reg \$auto$verilog_backend.cc:2083:dump_module$3  = 0;
  wire \$1 ;
  wire \$10 ;
  wire [9:0] \$12 ;
  wire [9:0] \$13 ;
  wire \$15 ;
  wire \$17 ;
  wire \$19 ;
  wire [8:0] \$21 ;
  wire [8:0] \$22 ;
  wire \$24 ;
  wire \$26 ;
  wire \$28 ;
  wire \$3 ;
  wire \$30 ;
  wire [3:0] \$5 ;
  wire [3:0] \$6 ;
  wire \$8 ;
  reg [2:0] _bit_index = 3'h0;
  reg [2:0] \_bit_index$next ;
  reg [7:0] addr = 8'h00;
  reg [7:0] \addr$next ;
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
  wire we;
  assign \$10  = \$8  & sck_edge_out;
  assign \$13  = { data, 1'h0 } + mosi;
  assign \$15  = ~ cs_n;
  assign \$17  = \$15  & sck_edge_out;
  assign \$1  = ~ cs_n;
  assign \$19  = _bit_index == 3'h7;
  assign \$22  = addr + 1'h1;
  assign \$24  = ~ cs_n;
  assign \$26  = \$24  & sck_edge_out;
  assign \$28  = _bit_index == 3'h7;
  assign \$30  = \$26  & \$28 ;
  always @(posedge clk)
    _bit_index <= \_bit_index$next ;
  always @(posedge clk)
    data <= \data$next ;
  always @(posedge clk)
    addr <= \addr$next ;
  assign \$3  = \$1  & sck_edge_out;
  assign \$6  = _bit_index + 1'h1;
  assign \$8  = ~ cs_n;
  sck_edge sck_edge (
    .clk(clk),
    .in_(sck_edge_in_),
    .out(sck_edge_out),
    .rst(rst)
  );
  always @* begin
    if (\$auto$verilog_backend.cc:2083:dump_module$3 ) begin end
    \_bit_index$next  = _bit_index;
    casez (\$3 )
      1'h1:
          \_bit_index$next  = \$6 [2:0];
    endcase
    casez (rst)
      1'h1:
          \_bit_index$next  = 3'h0;
    endcase
  end
  always @* begin
    if (\$auto$verilog_backend.cc:2083:dump_module$3 ) begin end
    \data$next  = data;
    casez (\$10 )
      1'h1:
          \data$next  = \$13 [7:0];
    endcase
    casez (rst)
      1'h1:
          \data$next  = 8'h00;
    endcase
  end
  always @* begin
    if (\$auto$verilog_backend.cc:2083:dump_module$3 ) begin end
    \addr$next  = addr;
    casez (\$17 )
      1'h1:
          casez (\$19 )
            1'h1:
                \addr$next  = \$22 [7:0];
          endcase
    endcase
    casez (rst)
      1'h1:
          \addr$next  = 8'h00;
    endcase
  end
  assign \$5  = \$6 ;
  assign \$12  = \$13 ;
  assign \$21  = \$22 ;
  assign we = \$30 ;
  assign sck_edge_in_ = sck;
endmodule

