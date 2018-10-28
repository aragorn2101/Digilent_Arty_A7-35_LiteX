# SW_BTN_All_LEDs SoC

Bit stream file at build > gateware > top.bit

Scripts are run using following protocol:
```
litex_server uart /dev/ttyUSB1 &
python3 script.py
```
Just replace /dev/ttyUSB1 with the block device identifier for your
board.


## Scripts descriptions

* ### btn_brightness

Small script which increases/decreases the brightness of the 4 RGB
LEDs. The colour is blue by default and the initial PWM level is
16 over 255. We consider 32 as a maximum and 0 as a minimum (off).

BTN1: decrease brightness<br/>
BTN2: increase brightness<br/>


* ### formula1_lights

This script simulates the Formula 1 Grand Prix starting lights scheme.
The 4 red LEDs are successively switched on at 1s interval. After the
fourth and last red light comes on, there is a random time interval
before the 4 lights are switched off altogether.

When started, the script displays messages at the command line and
waits for the user to press BTN3 for a countdown to start.


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

