# Test of the analog-to-digital conversion, for use in troubleshooting the laser harp
# Written by Scott Feister
#
# Uses the MCP3008 ADC

# Must install the MCP3008 python package first. Software SPI, not hardware.
# Follow MCP3008 instructions at: https://learn.adafruit.com/raspberry-pi-analog-to-digital-converters/mcp3008

# from time import sleep
import numpy as np
from Adafruit_MCP3008 import MCP3008

################## INITIALIZATION ###########################
  
## SET UP THE MCP3008 ADC
# Software SPI configuration:
CLK  = 4
MISO = 17 # a.k.a. DOUT
MOSI = 27 # a.k.a. DIN
CS   = 22 # a.k.a. CS/SHDN
mcp = MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

# Allocate arrays for ADC values
nchans = 8 # Number of analog input channels on the MCP3008
raw = np.zeros((nchans,), dtype=int) # The raw ADC values

# Set up a pretty printer of ADC values
printer = np.vectorize(lambda x: str(x).zfill(4)) # Call to print raw ADC values

########## CONTINUOUS PRINT VALUES TO TERMINAL ################

while True:
    # Read the ADC values
    for i in range(nchans):
        raw[i] = mcp.read_adc(i)
    # Print the ADC values to the terminal window
    print(printer(raw).astype('object'))