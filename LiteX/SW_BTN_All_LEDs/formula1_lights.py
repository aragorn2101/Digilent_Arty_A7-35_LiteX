#
#  formula1_lights.py
#
#  Script to simulate the Formula 1 lights scheme at the
#  start countdown.
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
from random import seed,random
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


# Initialise RNG
seed()


# Standard red duty : range(0,32)
RED_DUTY = 20

print("\n\n-- Formula 1 start lights procedure --")
print("\nWaiting for BTN3 to be activated.")


while True:
    sleep(0.2)
    button3 = wb.regs.button3_in.read()

    # If BTN3 is pressed, start countdown
    if (button3):
        # Generate a random time for the lights out procedure
        # Between 1.2s and 2.2s
        LIGHTS_OUT = random() + 1.2

        print("Starting countdown in 3s ...")
        sleep(3.0)
        wb.regs.rgbled3_r_duty.write(RED_DUTY)
        sleep(1.0)
        wb.regs.rgbled2_r_duty.write(RED_DUTY)
        sleep(1.0)
        wb.regs.rgbled1_r_duty.write(RED_DUTY)
        sleep(1.0)
        wb.regs.rgbled0_r_duty.write(RED_DUTY)
        sleep(LIGHTS_OUT)

        print("Lights out!")
        wb.regs.rgbled3_r_duty.write(0)
        wb.regs.rgbled2_r_duty.write(0)
        wb.regs.rgbled1_r_duty.write(0)
        wb.regs.rgbled0_r_duty.write(0)

        print("Lights were switched off after {:f} s.".format(LIGHTS_OUT))

        sleep(3.0)
        print("\n\n-- Formula 1 start lights procedure --")
        print("\nWaiting for BTN3 to be activated.")


wb.close()
