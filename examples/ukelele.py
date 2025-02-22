#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ukelele.py: High-tuning four-string laser uklele with five chord buttons

Created by Scott Feister, circa Feb 2025
"""

from twang import LightString, LightInstrument, ChordButton, getnote
import ulab.numpy as np
import board

# High ukelele tuning: G4-C4-E4-A4
OPEN_NAMES = ["G4","C4","E4","A4"]
OPEN_NOTES = [getnote(name) for name in OPEN_NAMES]


### RELATIVE CHORDS (based on frets)
x = -9999

# Basic chords: https://learnplayuke.com/chords-you-should-know/
C = [0,0,0,3] # Note that numbers denote fret #, not finger #
F = [2,0,1,0]
G = [0,2,3,2]
Am = [2,0,0,0]
A = [2,1,0,0]
D = [2,2,2,0]
Em = [0,4,3,2]
E = [1,4,0,2]


def shift_notes(notes, shifts):
    """ Shift a list of notes by a number of half-steps """
    # TODO: Check assertions
    shifted_notes = np.array(notes, dtype=np.int16) + np.array(shifts, dtype=np.int16) # Add the shift in note onto the note itself
    return shifted_notes

if __name__ == "__main__":
    print("OPEN_NOTES (midi numbers for an open chord): {}".format(OPEN_NOTES))

    # Phototransistor pins for strings (low-note strings first)
    STRINGS = [
        LightString(pin=board.GP15, note=OPEN_NOTES[0]),
        LightString(pin=board.GP10, note=OPEN_NOTES[1]),
        LightString(pin=board.GP6, note=OPEN_NOTES[2]),
        LightString(pin=board.GP2, note=OPEN_NOTES[3]),
    ]

    # Button pins for chords, and their associated notes
    CHORD_BTNS = [
        ChordButton(pin=board.GP16, notes=shift_notes(OPEN_NOTES, C)),
        ChordButton(pin=board.GP17, notes=shift_notes(OPEN_NOTES, G)),
        ChordButton(pin=board.GP18, notes=shift_notes(OPEN_NOTES, Am)),
        ChordButton(pin=board.GP19, notes=shift_notes(OPEN_NOTES, F)),
        ChordButton(pin=board.GP20, notes=shift_notes(OPEN_NOTES, Em)),
    ]

    # Combine the buttons and strings together into an instrument!
    my_ukelele = LightInstrument(strings=STRINGS, chord_btns=CHORD_BTNS, beam_pin=board.GP14, midi_program=0, debug=False)
    my_ukelele.run()
