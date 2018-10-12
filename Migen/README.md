# Migen Projects

Projects source files written in Python v3 and making use of the Migen HDL
generator. Each script is a different project, which usually has a counterpart
in the VHDL/Verilog sections in repository Digilent_Arty_A7-35-HDL.

A Migen script is compiled by running the following in an appropriately set up
environment:
```
$ python3 SCRIPTNAME
```

A build directory will be created and will be populated with the .xpr, .bit
files, along with all the usual Vivado stuff. The bitstream file (top.bit) can
be loaded directly on the FPGA using Vivado Hardware Manager.

For the Migen documentation check out:
[Migen Manual](https://m-labs.hk/migen/manual/)


## Projects descriptions

* ### led_brightness

This was a small project aiming at the development of the debouncing code.
The brightness of the RGB LEDs are varied using 2 buttons which increase
or decrease the PWM duty cycle.

BTN1: decrease brightness<br/>
BTN2: increase brightness<br/>



* ### stopwatch

Binary stopwatch implemented using the 4 monochromatic LEDs, 4 RGB LEDs. *SW3* is
used to start and stop the counter. When the switch is in the up position, the
counter proceeds and the binary number represented by the LEDs increase. When
the switch is brought to the bottom position the counter stops. *BTN3* is used to
reset the counter to 0, meaning that all LEDs are switched off.  LD4 to LD7
represent respectively bits 0,1,2,3 of an 8-bit number.  LD0 to LD3 represent
respectively bits 4,5,6,7. Thus, a total of 255 seconds can be shown using the
LEDs.

SW3 up: start<br/>
SW3 down: stop<br/>
BTN3: reset<br/>



* ### traffic_lights

Program to simulate traffic lights using the RGB LEDs. LD1--LD3 are for cars
while LD0 is for pedestrians. LD0 switches between red and green. A complete
cycle takes around 1min 20s. The lights are green for cars for around 1
minute. A pedestrian presses *BTN3* to request crossing, bringing down the
waiting time.

BTN3: request crossing for pedestrian<br/>

LD0: pedestrian red/green<br/>
LD1: cars red<br/>
LD2: cars amber<br/>
LD3: cars green<br/>



* ### colour_chooser1

Program to simultaneously light up the 4 RGB LEDs to a colour
which the user chooses. The level of each colour is adjusted
using the buttons.

BTN2: R<br/>
BTN1: G<br/>
BTN0: B<br/>

The position of the switches of the same index determine if
the change is an increment or decrement. If the switch is up
the corresponding level will be increased when the button is
pressed, but decreased otherwise.

SW2: R<br/>
SW1: G<br/>
SW0: B<br/>

*e.g. If SW2 and SW0 are up, but SW1 is down,<br/>
when BTN2 will be pressed, level of R will increase,<br/>
when BNT0 will be pressed, level of B will increase,<br/>
but when BTN1 will be pressed, level of G will decrease.*

Initially, all the LEDs are off, i.e. PWM duty level 0.



* ### colour_chooser2

The program allows the user to light up each one of the four RGB
LEDs to any colour using different R, G and B combinations on
each LED.

The switches are used to activate the LEDs. If a switch is in up
position, the RGB LED with index corresponding to the switch will
be affected when the R, G and B levels are changed, or when the
reset button is pressed. If the switch is in the down position,
the corresponding LED will not be affected at all.

SW3: LD3<br/>
SW2: LD2<br/>
SW1: LD1<br/>
SW0: LD0<br/>

The buttons are used to change the R, G and B levels, and also to
reset *active* LEDs to 0 level (unlit).

BTN3: reset<br/>
BTN2: R<br/>
BTN1: G<br/>
BTN0: B<br/>

