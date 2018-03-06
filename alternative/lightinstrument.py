#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
lightinstrument.py: Class-based definitions of light-based instruments

Makes it possible to have multiple MCP3008 for over 8 strings on the instrument

TODO: Possibly, decouple the read of the MCP values from the laser strings (if we find delay is too great for multiple strings)

Created by Scott Feister on Mon Mar  5 12:49:24 2018
"""

import os
from time import sleep
from datetime import datetime
import numpy as np
import pyo
from Adafruit_MCP3008 import MCP3008
from gpiozero import LED, Button

class LightInstrument:
    """
    Class for a musical instrument played by breaking beams of light.
    
    A LightInstrument incorporates several LightStrings.
    Example: A laser harp, or an LED-based piano.
    """
    self.lstrings = None # A list of LightString objects
    self.nstrings = None # The number of LightStrings
    def __init__(self, lstrings):
        self.nstrings = len(lstrings) # Count the number of strings

        ## INITIALIZE THE PYO SOUND MIXER
        s = pyo.Server(duplex=0).boot() # Boot the pyo server
        s.start()
        self.pyo_server = s
        
    def calibrate(self):
        """ Turn on/off lights and compute each beam's ADC value threshold for calling beam 'broken'"""
        # Turn on all the lights and record "On" ADC values
        for i in range(self.nstrings):
            self.lstrings[i].led.on()

        sleep(0.75) # Give lights a moment to fully turn on
        
        for i in range(self.nstrings):
            self.lstrings[i].on_adc = self.lstrings[i].read() # Record "On" values
        
        # Turn off all the lights and record "Off" ADC values
        for i in range(self.nstrings):
            self.lstrings[i].led.off()
            
        sleep(0.5) # Give lights a moment to fully turn off

        for i in range(self.nstrings):
            self.lstrings[i].off_adc = self.lstrings[i].read() # Record "Off" values
            
        # Calculate threshold ADC values (threshold for calling the light beam 'broken') as halfway between "On" and "Off". Then, turn lights back on.
        for i in range(self.nstrings):
            on_adc = self.lstrings[i].on_adc
            off_adc = self.lstrings[i].off_adc
            self.lstrings[i].thresh_adc = off_adc + (on_adc - off_adc) * 0.5 # Calculate an ADC threshold for broken light beam
            self.lstrings[i].led.on() # Turn lights back on
            
    
class LightString:
    """
    Class describing a single beam of light, its detector, and its sound
       
    Several packages are used for 
        Emitting light: gpiozero LED class, for emitting beam of light
        Receiving light: MCP3008 class analog-to-digital converter, and corresponding channel
        Sound: pyo server instance, audio filename
    """
    self.led = None # LED output from the gpiozero LED class
    self.mcp = None # Python instance of the analog-to-digital converter, MCP3008
    self.mcp_chan = None # Channel number on the ADC
    self.soundpath = None # Full file path to sound file, which will be played upon pluck
    self.SfPlayer = None # Pyo object of type SfPlayer. ("Soundfile Player")
    self.t_pluck = None # Time of the most recent pluck
    self.t_read = None # Time of the most ADC read
    self.pluckhold = None # Maximum seconds between subsequent plucks
    self.off_adc = None # Value of the ADC when light is off
    self.on_adc = None # Value of the ADC when light is on
    self.thresh_adc = None # Threshold, in ADC units, above which a pluck is valid
    self.val_adc = None
    
    def __init__(self, led, mcp, mcp_chan, soundpath, pluckhold=0.1):
        self.t_pluck = datetime.now() # Would be better if this were 1970
        self.pluckhold = pluckhold # TODO: Check that value is reasonable 
        
    def read(self):
        """ Read ADC value, and update time of most recent read """
        self.val_adc = self.mcp.read_adc(self.mcp_chan)
        self.t_read = datetime.now() # Update the time of most recent read
        return self.val_adc
        
    def pluck(self):
        """ Play sound, and update time of most recent pluck """
        self.SfPlayer.out() # Play the note
        self.t_pluck = datetime.now() # Update the time of the most recent pluck
    
    def read_and_pluck(self):
        """ Check beam and play sound (if appropriate)
        Only play sound if enough time has passed since last pluck.
        """       
        self.read() # Update the ADC values
        
        beamIsBroken = (self.val_adc > self.thresh_adc) # True or False, based on whether or not the ADC values exceed the threshold for a blocked light beam
        enoughTimePassed = (self.t_read - self.t_pluck).total_seconds() > self.pluckhold # True or False, based on whether enough time has passed since the last pluck of this string
        
        if beamIsBroken and enoughTimePassed:
            self.pluck()
            return True
        else:
            return False
        
if __name__ == "__main__":
    s1 = LightString()
