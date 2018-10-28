#
#  switch_rgbleds_off.py
#
#  Script to switch all RGB LEDs off.
#


from litex.soc.tools.remote import RemoteClient

wb = RemoteClient()
wb.open()

duty = [0 for i in range(12)]
colours = ['r', 'g', 'b']


# Read the current states of the LEDs
duty[0] = wb.regs.rgbled0_r_duty.read()
duty[1] = wb.regs.rgbled0_g_duty.read()
duty[2] = wb.regs.rgbled0_b_duty.read()
duty[3] = wb.regs.rgbled1_r_duty.read()
duty[4] = wb.regs.rgbled1_g_duty.read()
duty[5] = wb.regs.rgbled1_b_duty.read()
duty[6] = wb.regs.rgbled2_r_duty.read()
duty[7] = wb.regs.rgbled2_g_duty.read()
duty[8] = wb.regs.rgbled2_b_duty.read()
duty[9] = wb.regs.rgbled3_r_duty.read()
duty[10] = wb.regs.rgbled3_g_duty.read()
duty[11] = wb.regs.rgbled3_b_duty.read()

print("Initial states of RGB LEDs:")
for i in range(0,4):
    for j in range(0,3):
        print("RGBLED{:d}_{:s} duty = {:d}".format(i, colours[j], duty[3*i + j]))

# Light up the LEDs
print("Switching off all RGB LEDs ...")
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
