#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
instrument.py: Object-oriented approach to light-based instruments on Raspberry Pi Pico microcontrollers.

Example "Light Instruments" you can build with this library:
* Laser/LED Harp
* Laser/LED Banjo
* Laser/LED Ukelele
* Laser/LED Guitar

In Twang, a "LightInstrument" polls for plucks or strums of its "LightStrings" and sends MIDI messages to play sounds accordingly.
Optionally, you can add "ChordButtons" which, while depressed, temporarily shift the notes of the "LightStrings".

For use with the Pi Pico and CircuitPython.
  
Created by Scott Feister June 28, 2024.
"""

from time import sleep
import ulab.numpy as np
import board
import keypad
from digitalio import DigitalInOut, Direction, Pull
import usb_midi
import adafruit_midi
from adafruit_midi.note_off import NoteOff
from adafruit_midi.note_on import NoteOn
from adafruit_midi.program_change import ProgramChange

class LightInstrument:
    """
    Class for a musical instrument played by breaking beams of light.
    
    A LightInstrument incorporates several LightStrings, and, optionally, several ChordButtons (for changing chords).
    Example: A laser harp, an LED-based piano, or a laser guitar.
    """

    def __init__(self, strings, open_chord=None, chord_btns=None, beam_pin=board.GP2, midi_program=None, midi_channel=0, debug=False):
        """ If open_chord is specified, overrides the string values """

        self.debug = debug
        self.num_strings = len(strings) # Count the number of strings
        self.strings = strings # A list of LightString objects
        self.chord_btns = chord_btns # A list of ChordButton objects; if None, assume this is a harp-like instrument (no chord changes)
        self.beam_pin = beam_pin # The GPIO output pin that controls the light source for the strings (e.g. the pin that controls the lasers)
                    
        # Set up the light source pin as an output
        self.beam = DigitalInOut(self.beam_pin)
        self.beam.direction = Direction.OUTPUT
        
        self.midi = adafruit_midi.MIDI(midi_out=usb_midi.ports[1], out_channel=midi_channel)
        
        if midi_program is not None: # if unset, leave the midi program selection alone
            self.midi.send(ProgramChange(midi_program, channel=midi_channel))
        
        for string in strings:
            if not string.midi:
                string.midi = self.midi
        
        # Do a little blinky show
        for i in range(4):
            self.beam.value = True # Turn on/off light source for the strings (e.g. turn on/off the lasers)
            sleep(0.1)
            self.beam.value = False
            sleep(0.1)

        # Initialize notes on the strings with an open chord
        if open_chord is None:
            self.open_chord = [string.note for string in strings] # The default chord is pulled from the strings as configured right now
        else:
            self.open_chord = open_chord
        
        self.update_notes(self.open_chord)
        
        if chord_btns is not None:
            # Check that there are equal number of notes in all chords as there are strings!
            if len(self.open_chord) != len(strings):
                raise Exception("Number of notes in the open_chord does not match the number of LightStrings in the LightInstrument!")
            else:
                for chord_btn in chord_btns:
                    if len(chord_btn.notes) != len(strings):
                        raise Exception("Number of notes in ChordButton's chord does not match the number of LightStrings in the LightInstrument!")                

            # Initialize chord activation array to all False (nothing pressed)
            self.chord_status = np.array([False for btn in self.chord_btns]) # A True/False list of whether chord buttons are pressed
        
    def run(self):
        """ Begins endless loop of the instrument """           
        # Play an intro diddy
        self.strings[0].play()

        print("Instrument starting, ready to play!")
        self.beam.value = True # Turn on light source for the strings (e.g. turn on the lasers)
            
        while True:
            # Check for chord changes, and if so,
            #     update strings' notes
            self.check_for_chord_change()
            
            # Check if any strings have been plucked,
            #      and if so, send midi messages
            for string in self.strings:
                string.check_and_play()
    
    def update_notes(self, notes):
        """ Update the instrument's notes, e.g. when shifting chords """           
        for note, string in zip(notes, self.strings):
            string.change_note(note)
                                
    def check_for_chord_change(self):
        """ Update the currently implemented chord, only if new button has been pressed """
        if self.chord_btns is not None:
            chord_status = np.array([btn.is_pressed() for btn in self.chord_btns]) # List of True/False on whether buttons are pressed
            if np.sum((chord_status - self.chord_status)**2) > 0:
                # Update the chord array for future comparison
                self.chord_status = chord_status
    
                # Find the new chord notes
                if not np.any(chord_status):
                    notes = self.open_chord # No buttons pressed; use the open chord nontes
                    if self.debug:
                        print("Changing to open chord.")
                else:
                    ix = np.argmax(chord_status) # Index of the depressed chord (first occurrence), if applicable
                    notes = self.chord_btns[ix].notes
                    if self.debug:
                        print("Changing to chord #{}.".format(ix))

                # Apply the new chord notes to the strings
                self.update_notes(notes)
                                
class ChordButton:
    """
    A single chord and the button that activates it.
    Optional for LightInstruments.
    
    Midi note values less than -1 are ignored in Twang.
    """
    def __init__(self, pin, notes, debug=False):
        self.debug = debug
        
        self.notes = notes # A list of midi notes in this chord. E.g. notes = [12, 18, 19, 30, 41]. Should match number of strings. 

        notes_set = set([x for x in notes if x > -1]) # Exclude negative numbers, as these are assumed to be unusable later in the code
            
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
    A single string in the LightInstrument
    
    Includes the beam of light, photodetector, and its assigned midi note
    """
    
    def __init__(self, pin, note=72, midi=None, debug=False):
        self.debug = debug
        self.pin = pin # "board" pin number for phototransistor
        self.midi = midi # "adafruit_midi" MIDI instance (if left as None, nothing will play)
        self.note = note # MIDI note
        self.last_note = self.note
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
            self.midi.send([msg_note_off, msg_note_on])

            self.last_note = self.note # Update the last_note variable
            
    def check_and_play(self):
        event = self.keys.events.get() # event will be None if nothing has happened
        if event: # a string has either been pressed or released
            if event.pressed:
                # When string is pressed, mark down a timestamp and remain silent
                self.pressed_ticks_ms = event.timestamp  # timestamp, in milliseconds, for the press of the string
            if event.released:
                # When string is released, sound the note at a volume proportional to the time elapsed between press and release
                self.keys.events.clear()
                released_ticks_ms = event.timestamp # timestamp, in milliseconds, for the release of the string
                pluck_ms = released_ticks_ms - self.pressed_ticks_ms # The duration of the pluck is the millisecond difference between the press and release of the string
                # Note: unhandled overflow can occur here (empirically seen infrequently)
                
                # Scale the MIDI note velocity by the duration of the pluck. Plucking faster will make a louder sound.
                velocity = int(np.interp([pluck_ms], self.xp, self.yp)[0]) # Scale the velocity (arbitrary units of 0-127) to the pluck duration (milliseconds) using an interpolation function
                
                self.play(velocity=velocity) # play the sound by sending a MIDI message
                if self.debug:
                    print("Pluck detected!")
                    print("Pluck duration (ms): {}".format(pluck_ms))
                    print("Pluck velocity (0-127): {}".format(velocity))

if __name__ == "__main__":
    pass