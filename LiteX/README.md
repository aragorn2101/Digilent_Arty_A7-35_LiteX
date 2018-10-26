# LiteX projects

This directory contains the projects making use of the LiteX SoC builder.

For more information on LiteX check out:
[LiteX GitHub homepage](https://github.com/enjoy-digital/litex)

In every project, the top script will generally be named main.py, unless stated
otherwise in this README under the appropriate section.  When main.py is
executed using a python3 command from a LiteX environment the bitstream file is
generated. It is found at build > gateware > top.bit. This file can be loaded
on the board via USB UART using Vivado hardware manager. The SoC is then
controlled from the host computer itself using simple python scripts.

For accessing the SoC, first run the LiteX server need to be running in the
background:
```
litex_server uart /dev/ttyUSB1 &
```
/dev/ttyUSB1 is the block device on my computer. Check the content of /dev or
tail dmesg in order to find which block device needs to be used. Then, the test
scripts are simply executed using python3:
```
python3 script.py
```


## Projects descriptions

* ### test_1

A small project just to test LiteX with the Arty A7 FPGA.  Each test script has
a small description, near the top.


* ### SW_BTN_All_LEDs

This project builds an SoC binding the 4 switches, 4 buttons, 4 monochromatic LEDs
and all the r, g and b of the 4 RGB LEDs. Further details are given in the README
under the project directory.
