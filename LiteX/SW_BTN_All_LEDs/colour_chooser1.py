#
#  colour_chooser1.py
#
#  Program to freely choose colour of the four RGB LEDs
#
#  Copyright (C) 2018  Nitish Ragoomundun, Mauritius
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#


from time import sleep
from litex.soc.tools.remote import RemoteClient

wb = RemoteClient()
wb.open()



# Get SoC identifier
SoC_ID = ""
for i in range(256):
    c = chr(wb.read(wb.bases.identifier_mem + 4*i) & 0xff)
    SoC_ID += c
    if c == "\0":
        break
print("Identifier: " + SoC_ID)


# Array to store button and switch states
btn = [0, 0, 0]
sw  = [0, 0, 0]

# Array to hold duty levels for RGB LEDs
duty = [0, 0, 0]


while True:
    sleep(0.2)
    reset = wb.regs.button3_in.read()

    # If BTN3 is pressed, reset all RGB LEDs
    if (reset):
        duty = [0 for i in range(0,3)]
    else:
        # Read other buttons
        btn[0] = wb.regs.button2_in.read()
        btn[1] = wb.regs.button1_in.read()
        btn[2] = wb.regs.button0_in.read()

        # Read switches
        sw[0] = wb.regs.switch2_in.read()
        sw[1] = wb.regs.switch1_in.read()
        sw[2] = wb.regs.switch0_in.read()

        for i in range(0,3):
            duty[i] += (2*sw[i] - 1) * 2 * btn[i]

            # Normalise to a maximum of 32
            if (duty[i] > 32):
                duty[i] = 0
            if (duty[i] < 0):
                duty[i] = 32


        # Print the actual duty levels of R, G and B
        print("R: {:2d}\tG: {:2d}\tB: {:2d}".format(duty[0], duty[1], duty[2]))



    # Light up the LEDs
    wb.regs.rgbled0_r_duty.write(duty[0])
    wb.regs.rgbled0_g_duty.write(duty[1])
    wb.regs.rgbled0_b_duty.write(duty[2])
    wb.regs.rgbled1_r_duty.write(duty[0])
    wb.regs.rgbled1_g_duty.write(duty[1])
    wb.regs.rgbled1_b_duty.write(duty[2])
    wb.regs.rgbled2_r_duty.write(duty[0])
    wb.regs.rgbled2_g_duty.write(duty[1])
    wb.regs.rgbled2_b_duty.write(duty[2])
    wb.regs.rgbled3_r_duty.write(duty[0])
    wb.regs.rgbled3_g_duty.write(duty[1])
    wb.regs.rgbled3_b_duty.write(duty[2])


wb.close()
