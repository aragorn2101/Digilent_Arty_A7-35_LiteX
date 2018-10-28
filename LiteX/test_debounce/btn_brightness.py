#
#  btn_brightness.py
#
#  Script to decrease or increase brightness of a single colour
#  of the RGB LEDs using two buttons.
#


from time import sleep
from litex.soc.tools.remote import RemoteClient

wb = RemoteClient()
wb.open()


# Initialise all RGB LEDs with PWM duty 16
pwm_level = 16

while True:
    button0 = wb.regs.button0_deb_state.read()
    button1 = wb.regs.button1_deb_state.read()
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
