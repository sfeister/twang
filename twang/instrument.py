#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
instrument.py: Class-based definitions of light-based instruments on Raspberry Pi

Watches for plucks of light strings and pressing of buttons to change chords.
Uses Raspberry Pi's hardware interrupts on digital GPIO pins for catching quick plucks of strings.
Supports use of buttons to change chords ,facilitating not just laser harps, but laser guitars!

TODO:
    * Facilitate easier changing of instrument
    
Created by Scott Feister on Mon Aug  5 10:39:52 2019
Updated January 9, 2020 for use in DeAnza laser harp project.
"""

from datetime import datetime
import subprocess
from time import sleep
import numpy as np
import fluidsynth # sudo apt install fluidsynth; sudo pip3 install pyFluidSynth
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

class LightInstrument:
    """
    Class for a musical instrument played by breaking beams of light.
    
    A LightInstrument incorporates several LightStrings, and, optionally, several ChordButtons (for changing chords).
    Example: A laser harp, an LED-based piano, or a laser guitar.
    """

    def __init__(self, lstrings, open_chord=None, chordbtns=None, beampin=23, midi_instrument=0, driver="jack", soundfont="/usr/share/sounds/sf2/Guitars-Universal-V1.5.sf2", gain=0.2):
        """ If open_chord is specified, overrides the lstring values """

        self.nstrings = len(lstrings) # Count the number of strings
        self.lstrings = lstrings # A list of LightString objects
        self.chordbtns = chordbtns # A list of ChordButton objects; if None, assume this is a harp-like instrument (no chord changes)
        self.beampin = beampin # The GPIO output pin that controls the light source for the strings (e.g. the pin that controls the lasers)
        self.driver = driver # Valid entries for driver are "alsa" or "jack" -- gets fed into pyfluidsynth
        self.soundfont = soundfont # Path to the .sf2 soundfont file that you'd like to use
        self.midi_instrument = midi_instrument # midi instrument you'd like to use, within the 0th bank of this soundfont
        self.gain = gain # gain for fluidsynth that you'd like
        self.fs = None
        
        # Set up the light source pin as an output
        GPIO.setup(beampin, GPIO.OUT, initial=0)

        # Initialize notes on the lstrings with an open chord
        if open_chord is None:
            self.open_chord = [lstring.note for lstring in lstrings] # The default chord is pulled from the strings as configured right now
        else:
            self.open_chord = open_chord
        
        self.update_chord(self.open_chord)
        
        if chordbtns is not None:
            # Check that there are equal number of notes in all chords as there are lstrings!
            if len(self.open_chord) != len(lstrings):
                raise Exception("Number of notes in the open_chord does not match the number of LightStrings in the LightInstrument!")
            else:
                for chordbtn in chordbtns:
                    if len(chordbtn.notes) != len(lstrings):
                        raise Exception("Number of notes in ChordButton's chord does not match the number of LightStrings in the LightInstrument!")                

            # Initialize chord buttons array to all False (nothing pressed)
            self.chordarr = np.array([False for btn in self.chordbtns]) # A True/False list of whether chord buttons are pressed
        
    def start(self):
        """ Begins endless loop of the instrument """

        # Start fluidsynth and set instrument output
        print("Starting fluidsynth.")
        self.fs = fluidsynth.Synth(samplerate=48000, gain=self.gain, channels=1)
        self.fs.start(driver=self.driver)
        sfid = self.fs.sfload(self.soundfont)
        self.fs.program_select(0, sfid, 0, self.midi_instrument)

        if self.driver == "jack":
            # Make the jack audio connections of fluidsynth outputs to enable system playback
            subprocess.call(["jack_connect", "fluidsynth:l_00", "system:playback_1"])
            subprocess.call(["jack_connect", "fluidsynth:r_00", "system:playback_2"])
                
        # Play an intro diddy
        self.lstrings[0].play(self.fs)

        print("Instrument starting, ready to play!")
        GPIO.output(self.beampin, 1) # Turn on light source for the strings (e.g. turn on the lasers)

        for lstring in self.lstrings:
            lstring.start()
            
        while True:
            # Update the chord as needed
            self.check_and_update_chord()
            
            # Send MIDI signal for any strings that have been plucked since last loop iteration
            for lstring in self.lstrings:
                lstring.check_and_play(self.fs)
    
    def stop(self):
        for lstring in self.lstrings:
            lstring.stop()            

        GPIO.output(self.beampin, 0) # Turn off light source for the strings (e.g. turn off the lasers)
        self.fs.delete()
        self.fs = None


    def update_chord(self, chord):
        """ Update the currently implemented chord """
        for note, lstring in zip(chord, self.lstrings):
            lstring.change_note(note)
        
        self.chord = chord
                        
    def check_and_update_chord(self):
        """ Update the currently implemented chord, only if new button has been pressed """
        if self.chordbtns is not None:
            chordarr = np.array([btn.is_pressed() for btn in self.chordbtns]) # List of True/False on whether buttons are pressed
            if not np.array_equal(chordarr, self.chordarr):
                # Update the chord array for future comparison
                self.chordarr = chordarr
    
                # Find the new chord notes
                if not np.any(chordarr):
                    chord = self.open_chord # No buttons pressed; use the open chord
                else:
                    ix = np.argmax(chordarr) # Index of the depressed chord (first occurrence), if applicable
                    chord = self.chordbtns[ix].notes
                    
                # Apply the new chord notes to the lstrings
                self.update_chord(chord)
                        
    def __del__(self):
        self.stop()
        
class ChordButton:
    """
    Class describing a pushbutton that, when pressed, changes the chord
    
    -9999 is the only note allowed outside the integer range for midi notes.
    """
    def __init__(self, pin, midinotes):
        self.notes = midinotes # A list of midi notes in this chord. E.g. notes = [12, 18, 19, 30, 41]. Should match number of strings. 
        notes_set = set(midinotes)
        
        if -9999 in notes_set:
            notes_set.remove(-9999) # -9999 is a placeholder for non-pluckable string
            
        if not notes_set.issubset(set(range(128))): # Check that notes list contains only valid midi notes
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
    
    def __init__(self, pin, midinote=72, pluckhold=100):
        self.pin = pin # BCM pin number for phototransistor, on the Raspberry Pi
        self.pluckhold = pluckhold # Maximum milliseconds between subsequent plucks, implemented as a bouncetime in GPIO interrupt
        self.t_pluck = datetime.now() # Time of the most recent pluck (will just say now)
        self.last_note = midinote # MIDI note
        self.note = midinote # MIDI note
        self.playme = False # Whether or not to play the note at next opportunity
        
        # GPIO set up as an input, pulled up
        # (Button will be connected to GND on button press) 
        # TODO: Set this correctly for phototransistors
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

    def play(self, fs):
        """ Play sound using the Fluidsynth Midi player"""
        if self.note > -1: # Exclude case of -9999, which we are using to represent an unpluckable note
            fs.noteoff(0, self.last_note) # Stop playing old sound
            fs.noteon(0, self.note, vel=127) # Play new sound
            self.last_note = self.note # Update the last_note variable
    
    def check_and_play(self, fs):
        """ Check beam and play sound (if appropriate)
        Only play sound if it is waiting to be played.
        """       
        if self.playme:
            self.playme = False
            self.play(fs)
            
    def __del__(self):
        """ Shut down the string """
        self.stop()

if __name__ == "__main__":
    pass