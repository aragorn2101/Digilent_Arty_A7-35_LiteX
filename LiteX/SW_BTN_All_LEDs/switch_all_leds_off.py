#
#  switch_rgbleds_off.py
#
#  Script to switch all LEDs off.
#


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


# Array to store LED values
LED = [0 for i in range(16)]
RGB = ["r", "g", "b"]

# Read initial values of LEDs
LED[0] = wb.regs.monoled0_out.read()
LED[1] = wb.regs.monoled1_out.read()
LED[2] = wb.regs.monoled2_out.read()
LED[3] = wb.regs.monoled3_out.read()
LED[4] = wb.regs.rgbled0_r_duty.read()
LED[5] = wb.regs.rgbled0_g_duty.read()
LED[6] = wb.regs.rgbled0_b_duty.read()
LED[7] = wb.regs.rgbled1_r_duty.read()
LED[8] = wb.regs.rgbled1_g_duty.read()
LED[9] = wb.regs.rgbled1_b_duty.read()
LED[10] = wb.regs.rgbled2_r_duty.read()
LED[11] = wb.regs.rgbled2_g_duty.read()
LED[12] = wb.regs.rgbled2_b_duty.read()
LED[13] = wb.regs.rgbled3_r_duty.read()
LED[14] = wb.regs.rgbled3_g_duty.read()
LED[15] = wb.regs.rgbled3_b_duty.read()


# Print values
print("\nInitial LED values:")
for i in range(0,4):
    print("{:s}{:d} : {:d}".format("monoled", i, LED[i]))
for i in range(0,4):
    for j in range(0,3):
        print("{:s}{:d}{:s} : {:d}".format("rgbled_", i, "_"+RGB[j], LED[3*i + j + 4]))


# Switch off all LEDs
print("\nSwitching off all LEDs ...")
wb.regs.monoled0_out.write(0)
wb.regs.monoled1_out.write(0)
wb.regs.monoled2_out.write(0)
wb.regs.monoled3_out.write(0)
wb.regs.rgbled0_r_duty.write(0)
wb.regs.rgbled0_g_duty.write(0)
wb.regs.rgbled0_b_duty.write(0)
wb.regs.rgbled1_r_duty.write(0)
wb.regs.rgbled1_g_duty.write(0)
wb.regs.rgbled1_b_duty.write(0)
wb.regs.rgbled2_r_duty.write(0)
wb.regs.rgbled2_g_duty.write(0)
wb.regs.rgbled2_b_duty.write(0)
wb.regs.rgbled3_r_duty.write(0)
wb.regs.rgbled3_g_duty.write(0)
wb.regs.rgbled3_b_duty.write(0)


wb.close()
