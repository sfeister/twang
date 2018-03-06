# Test of the calibration of the lasers
# Written by Scott Feister
#
# Uses the MCP3008 ADC, photoresistors + 10k resistors, 

# Must install the MCP3008 python package first. Software SPI, not hardware.
# Follow MCP3008 instructions at: https://learn.adafruit.com/raspberry-pi-analog-to-digital-converters/mcp3008
# 
# Documentation on initializing LED, Button:
#   https://gpiozero.readthedocs.io/en/latest/recipes.html
# 
# TODO: Could make this better by putting in a graph, etc. during real-time presses

from time import sleep
import numpy as np
from Adafruit_MCP3008 import MCP3008
from gpiozero import LED, Button

################## INITIALIZATION ###########################    
def callback1():
    """ Button callback function, switches harp state to 'calibrate' """
    global state
    state = 'calibrate'

## SET UP THE MCP3008 ADC
# Software SPI configuration:
CLK  = 4
MISO = 17 # a.k.a. DOUT
MOSI = 27 # a.k.a. DIN
CS   = 22 # a.k.a. CS/SHDN
mcp = MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

## INITIALIZE THE LASER CONTROL and CALIBRATE BUTTON
LAS = 23 # Pin on which laser circuit is relayed
lasers = LED(LAS) # Initialize the laser as LED-style digital I/O
lasers.on() # Turn on the lasers

BTN = 24
button = Button(BTN)
button.when_pressed = callback1

## SET SOME BASIC INFO
nstrings = 5 # Number of harp strings

# Allocate arrays for ADC values
raw = np.zeros((nstrings,), dtype=int) # The raw ADC values
thresh_raw = np.zeros_like(raw)

# Set up a pretty printer of ADC values
printer = np.vectorize(lambda x: str(x).zfill(4)) # Call to print raw ADC values


################## TESTING STATE MACHINE ###########################
state = 'wait' # Start in the 'wait' state

while True:
    if state == 'calibrate':
        print("Test calibrating (no button press needed)...")
        lasers.on()
        sleep(0.75) # Give lasers a moment to fully turn on

        for i in range(nstrings):
            raw[i] = mcp.read_adc(i)

        raw_on = np.copy(raw)
        print("Lasers on: ")
        print(printer(raw_on).astype('object'))

        lasers.off()
        sleep(0.5) # Give lasers a moment to fully turn off

        for i in range(nstrings):
            raw[i] = mcp.read_adc(i)

        raw_off = np.copy(raw)
        print("Lasers off: ")
        print(printer(raw_off).astype('object'))

        thresh_raw = raw_off + (raw_on - raw_off) * 0.5
        print("Triggering below: ")
        print(printer(thresh_raw).astype('object'))

        percent_drop = ((raw_on - raw_off)*100)/raw_on # Percentage of the signal that was dropped during calibration
        print("DEBUG SUMMARY: Percent drop from on to off (closer to 100 is better): ")
        print(printer(percent_drop).astype('object'))

        print("Test calibration complete!")
        
        state = 'wait'  # Switch into the 'wait' state
        
    elif state == 'wait': # Default state, where nothing happens
        sleep(0.1) # Do nothing; just keep waiting for a button press
