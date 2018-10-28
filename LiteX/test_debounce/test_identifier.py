#
#  test_identier.py
#
#  Test script to print the identifier for the SoC
#  present on the board.
#

from litex.soc.tools.remote import RemoteClient

wb = RemoteClient()
wb.open()

# # #

# get identifier
fpga_id = ""
for i in range(256):
    c = chr(wb.read(wb.bases.identifier_mem + 4*i) & 0xff)
    fpga_id += c
    if c == "\0":
        break
print("fpga_id: " + fpga_id)

# # #

wb.close()
