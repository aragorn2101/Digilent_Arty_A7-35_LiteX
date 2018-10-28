#
#  colour_chooser2.py
#
#  Program to light up each of the 4 RGB LEDs individually with any colour
#  combination.
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
sw  = [0, 0, 0, 0]

# Array to hold duty levels for RGB LEDs
duty = [0 for i in range(12)]


while True:
    sleep(0.2)
    reset = wb.regs.button3_in.read()

    # If BTN3 is pressed, reset all RGB LEDs
    if (reset):
        for i in range(0,3):
            for j in range(0,4):
                if (sw[j]):
                    duty[i + 3*j] = 0
    else:
        # Read other buttons
        btn[0] = wb.regs.button2_in.read()
        btn[1] = wb.regs.button1_in.read()
        btn[2] = wb.regs.button0_in.read()

        # Read switches
        sw[0] = wb.regs.switch0_in.read()
        sw[1] = wb.regs.switch1_in.read()
        sw[2] = wb.regs.switch2_in.read()
        sw[3] = wb.regs.switch3_in.read()

        for i in range(0,3):
            for j in range(0,4):
                duty[i + 3*j] += 2*btn[i]*sw[j]

                # Normalise to a maximum of 32
                if (duty[i + 3*j] > 32): duty[i + 3*j] = 0
                if (duty[i + 3*j] < 0):  duty[i + 3*j] = 32


        # Print the actual duty levels of R, G and B
        print("(R,G,B)\t:\tLD3({led3_r:2d},{led3_g:2d},{led3_b:2d})\tLD2({led2_r:2d},{led2_g:2d},{led2_b:2d})\tLD1({led1_r:2d},{led1_g:2d},{led1_b:2d})\tLD0({led0_r:2d},{led0_g:2d},{led0_b:2d})"
                .format(led3_r = duty[9], led3_g = duty[10], led3_b = duty[11],
                        led2_r = duty[6], led2_g = duty[7],  led2_b = duty[8],
                        led1_r = duty[3], led1_g = duty[4],  led1_b = duty[5],
                        led0_r = duty[0], led0_g = duty[1],  led0_b = duty[2]))



    # Light up the LEDs
    wb.regs.rgbled0_r_duty.write(duty[0])
    wb.regs.rgbled0_g_duty.write(duty[1])
    wb.regs.rgbled0_b_duty.write(duty[2])
    wb.regs.rgbled1_r_duty.write(duty[3])
    wb.regs.rgbled1_g_duty.write(duty[4])
    wb.regs.rgbled1_b_duty.write(duty[5])
    wb.regs.rgbled2_r_duty.write(duty[6])
    wb.regs.rgbled2_g_duty.write(duty[7])
    wb.regs.rgbled2_b_duty.write(duty[8])
    wb.regs.rgbled3_r_duty.write(duty[9])
    wb.regs.rgbled3_g_duty.write(duty[10])
    wb.regs.rgbled3_b_duty.write(duty[11])


wb.close()
