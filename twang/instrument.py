#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
instrument.py: Class-based definitions of light-based instruments on Raspberry Pi Pico microcontrollers.

Outputs MIDI, one string per channel.

Watches for plucks of light strings and pressing of buttons to change chords.
Supports use of buttons to change chords ,facilitating not just laser harps, but laser guitars!

For use with the Pi Pico and CircuitPython.

TODO:
    * Facilitate easier changing of instrument
    
Created by Scott Feister June 28, 2024.
"""

from time import sleep
import ulab.numpy as np
import board
import keypad
from digitalio import DigitalInOut, Direction, Pull
import pulseio
import usb_midi

import adafruit_midi
from adafruit_midi.note_off import NoteOff
from adafruit_midi.note_on import NoteOn

class LightInstrument:
    """
    Class for a musical instrument played by breaking beams of light.
    
    A LightInstrument incorporates several LightStrings, and, optionally, several ChordButtons (for changing chords).
    Example: A laser harp, an LED-based piano, or a laser guitar.
    """

    def __init__(self, lstrings, open_chord=None, chordbtns=None, beampin=board.GP2):
        """ If open_chord is specified, overrides the lstring values """

        self.nstrings = len(lstrings) # Count the number of strings
        self.lstrings = lstrings # A list of LightString objects
        self.chordbtns = chordbtns # A list of ChordButton objects; if None, assume this is a harp-like instrument (no chord changes)
        self.beampin = beampin # The GPIO output pin that controls the light source for the strings (e.g. the pin that controls the lasers)
                    
        # Set up the light source pin as an output
        self.beam = DigitalInOut(self.beampin)
        self.beam.direction = Direction.OUTPUT
        
        self.midi = adafruit_midi.MIDI(midi_out=usb_midi.ports[1], out_channel=0)
        for lstring in lstrings:
            if not lstring.midi:
                lstring.midi = self.midi
        
        # Do a little blinky show
        for i in range(4):
            self.beam.value = True # Turn on/off light source for the strings (e.g. turn on/off the lasers)
            sleep(0.1)
            self.beam.value = False
            sleep(0.1)

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
        
    def run(self):
        """ Begins endless loop of the instrument """           
        # Play an intro diddy
        self.lstrings[0].play()

        print("Instrument starting, ready to play!")
        self.beam.value = True # Turn on light source for the strings (e.g. turn on the lasers)

        #for lstring in self.lstrings:
        #    lstring.start()
            
        while True:
            # Update the chord as needed
            self.check_and_update_chord() # TODO
            
            # Send MIDI signal for any strings that have been plucked since last loop iteration
            for lstring in self.lstrings:
                lstring.check_and_play()
    
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
        
        self.dio = DigitalInOut(self.pin)
        self.dio.direction = Direction.INPUT
        self.dio.pull = Pull.UP
        
    def is_pressed(self):
        return not self.dio.value
        

class LightString:
    """
    Class describing a single beam of light and its interrupt
       
    """
    
    def __init__(self, pin, midinote=72, midi=None):
        self.pin = pin # "board" pin number for phototransistor
        self.midi = midi # "adafruit_midi" MIDI instance (if left as None, nothing will play)
        self.note = midinote # MIDI note
        self.last_note = self.note
        #self.pulses = pulseio.PulseIn(self.pin, maxlen=10, idle_state=False)
        self.keys = keypad.Keys((self.pin,), value_when_pressed=False, pull=True, interval=0.01)
        
        self.xp = np.logspace(np.log10(50), np.log10(500), num=20) # for interpolating pluck duration
        self.yp = np.linspace(127, 40, num=20)
        
    def change_note(self, note):
        """Update the note for the next pluck """
        self.note = note # Update the midi note without affecting currently-playing sounds

    def play(self, velocity=127):
        """ Play sound using the midi output"""
        if not self.midi:
            raise Exception("MIDI not initialized properly for this string, so we can't play anything.")
            
        if self.note > -1: # Exclude case of -9999, which we are using to represent an unpluckable string
            msg_note_off = NoteOff(self.last_note) # Stop playing old sound
            msg_note_on = NoteOn(self.note, velocity=velocity) # Play new sound
            self.last_note = self.note # Update the last_note variable
            self.midi.send([msg_note_off, msg_note_on])
            
    # Use pulse logic for getting a velocity on the strum
    def check_and_play(self):
        event = self.keys.events.get()
        # event will be None if nothing has happened.
        if event:
            if event.pressed:
                self.pressed_ticks_ms = event.timestamp
            if event.released:
                self.keys.events.clear()
                pluck_ms = event.timestamp - self.pressed_ticks_ms
                velocity = int(np.interp([pluck_ms], self.xp, self.yp)[0]) # Scale it down
                self.play(velocity=velocity) # TODO: Add in a velocity
                print("Pluck detected!") # DEBUG
                print("Pluck duration (ms): {}".format(pluck_ms)) # DEBUG
                print("Pluck velocity (0-127): {}".format(velocity)) # DEBUG

        # if len(self.pulses) > 0: # Check for a new pluck of this string
            # print("Pluck detected!") # DEBUG
            
            # self.pulses.pause()
            # npulses = len(self.pulses)
            # pulse_arr = np.zeros(npulses)
            # for i in range(len(self.pulses)):
                # pulse_arr[i] = self.pulses[i]

            # self.pulses.clear()
            # self.pulses.resume()
            # print("List of raw pulses (us): {}".format(pulse_arr)) # DEBUG
            # longest_active_us = np.max(pulse_arr[::2])
            # print("Pluck duration (us): {}".format(longest_active_us)) # DEBUG
            
            # # Play the pluck as midi, with corresponding velocity
            # self.play() # TODO: Add in a velocity


if __name__ == "__main__":
    pass