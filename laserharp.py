# Pi Instrument Script
# Written by Scott Feister
#
# Run this script to play your laser instrument!
# You might want to even add it into the startup menu.
#
# Start jack before running this script, e.g. via
#   export DISPLAY=:0 
#   jackd -d alsa -n 16 &
# 
#
# Uses the MCP3008 ADC, photoresistors + 10k resistors, 
#
# Must install the MCP3008 python package first. Software SPI, not hardware.
# Follow MCP3008 instructions at: https://learn.adafruit.com/raspberry-pi-analog-to-digital-converters/mcp3008
#
# Documentation on initializing LED, Button:
#   https://gpiozero.readthedocs.io/en/latest/recipes.html

import os
from time import sleep
from datetime import datetime
import numpy as np
import pyo
from Adafruit_MCP3008 import MCP3008
import Adafruit_GPIO.SPI as SPI
from gpiozero import LED, Button


################## INITIALIZATION ###########################
def callback1():
    """ Button callback function, switches harp state to 'calibrate' """
    global state
    state = 'calibrate'
    
## SET UP THE MCP3008 ADC
# Hardware SPI configuration:
SPI_PORT   = 0
SPI_DEVICE = 0
mcp = MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

#Software SPI
#CLK  = 4
#MISO = 17 # a.k.a. DOUT
#MOSI = 27 # a.k.a. DIN
#CS   = 22 # a.k.a. CS/SHDN
#mcp = MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

## INITIALIZE THE LASER CONTROL / CALIBRATION BUTTON
LAS = 23 # Pin on which laser circuit is relayed
lasers = LED(LAS) # Initialize the laser as LED-style digital I/O
lasers.on() # Turn on the lasers

BTN = 24
button = Button(BTN)
button.when_pressed = callback1 # Could change to "when_released"

## INITIALIZE THE SOUND MIXER
s = pyo.Server(duplex=0).boot() # Boot the pyo server
s.start()

## SET SOME BASIC INFO
nstrings = 5 # Number of harp strings
pluckhold = 0.1 # Maximum seconds between subsequent plucks

scriptdir = os.path.dirname(os.path.realpath(__file__)) # Directory of this script
notedir = os.path.join(scriptdir, "sounds", "guitar") # Directory containing list of audio files
#notedir = r"/home/pi/mycode/twang/sounds/guitar" # Directory containing list of audio files
notes = ["c4", "d4", "e4", "f4", "g4"]  # List of wav files in the notedir folder
ext = ".wav"

sounds = [None]*nstrings
tpluck = [None]*nstrings
holds = [None]*nstrings

for i in range(nstrings):
    sounds[i] = pyo.SfPlayer(os.path.join(notedir, notes[i] + ext))
    tpluck[i] = datetime.now() # Would be better if it was not now, but 1970
    holds[i] = False

sounds[0].out() # Greet the world by playing the low note

# Allocate arrays for ADC values
raw = np.zeros((nstrings,), dtype=int) # The raw ADC values
thresh_raw = np.zeros_like(raw)

# Set up a pretty printer of ADC values
printer = np.vectorize(lambda x: str(x).zfill(4)) # Call to print raw ADC values


################## HARP STATE MACHINE ###########################
state = 'calibrate' # Start machine in calibration state

while True:
    if state == 'calibrate':
        print("Calibrating...")
        lasers.on()
        sleep(0.75) # Give lasers a moment to fully turn on

        for i in range(nstrings):
            raw[i] = mcp.read_adc(i)

        raw_on = np.copy(raw)
        print("Lasers on: " + str(raw_on))
        
        lasers.off()
        sleep(0.5) # Give lasers a moment to fully turn off

        for i in range(nstrings):
            raw[i] = mcp.read_adc(i)

        raw_off = np.copy(raw)
        print("Lasers off: " + str(raw_off))
        thresh_raw = raw_off + (raw_on - raw_off) * 0.5
        print("Triggering below: " + str(thresh_raw))
        
        lasers.on()
        sleep(0.5) # Give lasers a moment to fully turn back on

        print("Calibration complete!")

        state = 'instrument'  # Switch into the 'instrument' state

    elif state == 'debug': # Currently unused
        for i in range(nstrings):
            raw[i] = mcp.read_adc(i)
        print(printer(raw).astype('object')) 
    
    elif state == 'instrument':
        ## POLL THE ADC FOR SIGNIFICANT CHANGES (AND PLAY NOTES)
        for i in range(nstrings):
            raw[i] = mcp.read_adc(i)

        for i in range(nstrings): # Empirically, this loop is plenty fast
            if (datetime.now() - tpluck[i]).total_seconds() > pluckhold:
                if raw[i] < thresh_raw[i]: # The value is less than the threshold
                    if not holds[i]:
                        print("Plucked " + str(notes[i]))
                        sounds[i].out() # Play the note
                        tpluck[i] = datetime.now()
                        holds[i] = True
                else:
                    holds[i] = False
