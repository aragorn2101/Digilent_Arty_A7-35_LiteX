
from migen import *

from litex.build.generic_platform import *
from litex.build.xilinx import XilinxPlatform

from litex.soc.integration.soc_core import *
from litex.soc.integration.builder import *

from litex.soc.cores.uart import UARTWishboneBridge

from litex.soc.interconnect.csr import *
from litex.soc.cores import gpio


class Button(Module, AutoCSR):
    def __init__(self, btn):
        self.submodules.deb = Debounce(btn)

class RGBLed(Module, AutoCSR):
    def __init__(self, pads):
        self.submodules.r = PWM(pads.r)
        self.submodules.g = PWM(pads.g)
        self.submodules.b = PWM(pads.b)


###  BEGIN module Debounce  ###
class Debounce(Module, AutoCSR):
    def __init__(self, button):
        self.state = CSRStorage()

        curr_state = Signal()
        idle = Signal()
        sync0 = Signal()
        sync1 = Signal()
        counter = Signal(18)

        # Initialise wires
        idle.eq(0)
        sync0.eq(0)
        sync1.eq(0)
        curr_state.eq(0)

        # Sequential code
        self.sync += [
                sync0.eq(button),
                sync1.eq(sync0),
                If ((idle),
                    counter.eq(0)
                ).Else (
                    counter.eq(counter + 1),
                    If (counter >= 249999,  # debounce on delay of 2.5 ms
                        curr_state.eq(~curr_state)
                    )
                )
        ]

        # Concurrent code
        self.comb += [
                idle.eq(curr_state == sync1),
                self.state.storage.eq(~idle & (counter >= 249999) & ~curr_state)
        ]
###  END module Debounce  ###



###  BEGIN module PWM  ###
class PWM(Module, AutoCSR):
    def __init__(self, LED):
        self.duty = CSRStorage(8)

        counter = Signal(8)  # 0 -- 255 : period

        # sequential code
        self.sync += [ counter.eq(counter + 1) ]

        # concurrent code
        self.comb += [ LED.eq( counter < self.duty.storage ) ]

###  END module PWM  ###



###  BEGIN Describe platform  ###
_io = [ ("CLK100MHZ", 0, Pins("E3"), IOStandard("LVCMOS33")),

        # Buttons
        ("button", 0, Pins("D9"), IOStandard("LVCMOS33")),
        ("button", 1, Pins("C9"), IOStandard("LVCMOS33")),

        # RGB LED0
        ("RGBled", 0, Subsignal("r", Pins("G6")), # R
                      Subsignal("g", Pins("F6")), # G
                      Subsignal("b", Pins("E1")), # B
                      IOStandard("LVCMOS33")),
        # RGB LED1
        ("RGBled", 1, Subsignal("r", Pins("G3")), # R
                      Subsignal("g", Pins("J4")), # G
                      Subsignal("b", Pins("G4")), # B
                      IOStandard("LVCMOS33")),
        # RGB LED2
        ("RGBled", 2, Subsignal("r", Pins("J3")), # R
                      Subsignal("g", Pins("J2")), # G
                      Subsignal("b", Pins("H4")), # B
                      IOStandard("LVCMOS33")),
        # RGB LED3
        ("RGBled", 3, Subsignal("r", Pins("K1")), # R
                      Subsignal("g", Pins("H6")), # G
                      Subsignal("b", Pins("K2")), # B
                      IOStandard("LVCMOS33")),

        # USB UART
        ("serial", 0, Subsignal("tx", Pins("D10")), # rxd_out
                      Subsignal("rx", Pins("A9")),  # txd_in
                      IOStandard("LVCMOS33"))
        ]


class Platform(XilinxPlatform):
    default_clk_name = "CLK100MHZ"
    default_clk_period = 10.00

    def __init__(self):
        XilinxPlatform.__init__(self, "xc7a35ticsg324-1L", _io, toolchain="vivado")

    def do_finalize(self, fragment):
        XilinxPlatform.do_finalize(self, fragment);

###  END Describe platform  ###



###  BEGIN Design  ###

def csr_map_update(csr_map, csr_peripherals):
    csr_map.update(dict((n, v)
        for v, n in enumerate(csr_peripherals, start=max(csr_map.values()) + 1)))

# create our platform (fpga interface)
platform = Platform()


# create our soc (fpga description)
class BaseSoC(SoCCore):

    # Peripherals CSR declaration
    csr_peripherals = [
        "button0",
        "button1",
        "rgbled0",
        "rgbled1",
        "rgbled2",
        "rgbled3",
        "serial"
    ]
    csr_map_update(SoCCore.csr_map, csr_peripherals)

    def __init__(self, platform, **kwargs):
        sys_clk_freq = int(100e6)

        # SoC init (No CPU, we control the SoC with UART)
        SoCCore.__init__(self, platform, sys_clk_freq,
            cpu_type=None,
            csr_data_width=32,
            with_uart=False,
            with_timer=False,
            ident="SoC with only RGB LEDs and buttons to test debounce.", ident_version=True,
            )

        # Clock Reset Generation
        self.submodules.crg = CRG(platform.request("CLK100MHZ"))


        # No CPU, use Serial to control Wishbone bus
        self.add_cpu_or_bridge(UARTWishboneBridge(platform.request("serial"), sys_clk_freq, baudrate=115200))
        self.add_wb_master(self.cpu_or_bridge.wishbone)

        # RGB LED
        self.submodules.rgbled0 = RGBLed(platform.request("RGBled", 0))
        self.submodules.rgbled1 = RGBLed(platform.request("RGBled", 1))
        self.submodules.rgbled2 = RGBLed(platform.request("RGBled", 2))
        self.submodules.rgbled3 = RGBLed(platform.request("RGBled", 3))

        # Buttons
        self.submodules.button0 = Button(platform.request("button", 0))
        self.submodules.button1 = Button(platform.request("button", 1))

###  END Design  ###


soc = BaseSoC(platform)

#
# build
#
builder = Builder(soc, output_dir="build", csr_csv="csr.csv")
builder.build()
