#
#  btn_brightness.py
#
#  Script to decrease or increase brightness of a single colour
#  of the RGB LEDs using two buttons.
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


# Initialise all RGB LEDs with PWM duty 16
pwm_level = 16

while True:
    sleep(0.2)
    button0 = wb.regs.button0_in.read() & 0x1
    button1 = wb.regs.button1_in.read() & 0x1

    print("BTN0 : {:1d}\tBTN1 : {:1d}".format(button0, button1))

    # If BTN0 is pressed decrease brightness
    if (button0):
        pwm_level -= 2

        if (pwm_level < 0):
            pwm_level = 32

    # If BTN1 is pressed increase brightness
    if (button1):
        pwm_level += 2
        if (pwm_level > 32):
            pwm_level = 0

    # Light up the LEDs
    wb.regs.rgbled0_b_duty.write(pwm_level)
    wb.regs.rgbled1_b_duty.write(pwm_level)
    wb.regs.rgbled2_b_duty.write(pwm_level)
    wb.regs.rgbled3_b_duty.write(pwm_level)


wb.close()
