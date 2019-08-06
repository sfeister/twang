#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LightInstrument4.py: Class-based definitions of light-based instruments outputting MIDI

Now using interrupts and support for chords.

Created by Scott Feister on Mon Aug  5 10:39:52 2019
"""


import os
from time import sleep
from datetime import datetime
import numpy as np
import pygame.midi
import RPi.GPIO as GPIO  
GPIO.setmode(GPIO.BCM)

class LightInstrument:
    """
    Class for a musical instrument played by breaking beams of light.
    
    A LightInstrument incorporates several LightStrings.
    Example: A laser harp, or an LED-based piano.
    """

    def __init__(self, lstrings, chordbtns=None):
        pygame.midi.init()
        self.player = pygame.midi.Output(0)
        self.player.set_instrument(0)

        self.nstrings = len(lstrings) # Count the number of strings
        self.lstrings = lstrings # A list of LightString objects
        self.chordbtns = chordbtns # A list of ChordButton objects
        
    def start(self):
        """ Begins endless loop of hearing the instrument """
        while True:
            self.update_chord()
            for lstring in self.lstrings:
                lstring.check_and_play(self.player)
    
    def update_chord(self):
        """ Update the currently implemented chord """
                    
    def __del__(self):
        del self.player
        pygame.midi.quit()
        GPIO.cleanup() # Not sure if this will work as hoped here...

class ChordButton:
    """
    Class describing a pushbutton that, when pressed, changes the chord
    """
    def __init__(self, pin, notes):
        self.notes = notes # A list of midi notes in this chord. E.g. notes = [12, 18, 19, 30, 41]. Should match number of strings. 
        if not set(notes).issubset(set(range(128))): # Check that notes list contains only valid midi notes
            raise Exception("Invalid notes. All midi notes must be integers the range of 0 to 127.")

        self.pin = pin # BCM pin number
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Pull-up; connect other side to GND

    def is_pressed(self):
        """ Get whether button is pressed """
        return not GPIO.input(self.pin)
    
class LightString:
    """
    Class describing a single beam of light and its interrupt
       
    """
    
    def __init__(self, pin, note=72, pluckhold=100):
        self.pin = pin # BCM pin number for phototransistor, on the Raspberry Pi
        self.pluckhold = pluckhold # Maximum milliseconds between subsequent plucks, implemented as a bouncetime in GPIO interrupt
        self.t_pluck = datetime.now() # Time of the most recent pluck (will just say now)
        self.last_note = note # MIDI note
        self.note = note # MIDI note
        self.playme = False # Whether or not to play the note at next opportunity
        
        # GPIO set up as an input, pulled up, connected to 3V3 on button press  
        # TODO: Set this correctly given our circuit
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
    def start(self):
        """ Start watching for plucks of this Light String """
        # Set up an interrupt on this pin
        GPIO.add_event_detect(self.pin, GPIO.FALLING, callback=self.callback, bouncetime=self.pluckhold)
    
    def stop(self):
        """ Stop watching for plucks of this Light String """
        GPIO.remove_event_detect(self.pin)
        
    def callback(self, channel):
        """ Interrupt callback for the pluck of this string 
        Note: Kept as quick as possible """
        self.t_pluck = datetime.now() # Update the time of the most recent pluck
        self.playme = True # Play note at next opportunity
        
    def change_note(self, note):
        """Update the note for the next pluck """
        self.note = note # Update the midi note without affecting currently-playing sounds

    def play(self, player):
        """ Play sound using the PyGame Midi player"""
        player.note_off(self.last_note, velocity=127) # Stop playing old sound
        player.note_on(self.note, velocity=127) # Play new sound
        self.last_note = self.note # Update the last_note variable
    
    def check_and_play(self, player):
        """ Check beam and play sound (if appropriate)
        Only play sound if it is waiting to be played.
        """       
        if self.playme:
            self.playme = False
            self.play()
            
    def __del__(self):
        """ Shut down the string """
        self.stop()

if __name__ == "__main__":
    s1 = LightString(pin=13)
