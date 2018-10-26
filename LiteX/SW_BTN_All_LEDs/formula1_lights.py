#
#  formula1_lights.py
#
#  Script to simulate the Formula 1 lights scheme at the
#  start countdown.
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
