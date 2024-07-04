#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
guitar.py: Standard-tuning six-string laser guitar with four laser buttons

Created by Scott Feister on Tue Aug 13 20:08:07 2019
"""

#from lightinstrument4 import LightInstrument, ChordButton, LightString
from twang import LightString, LightInstrument, ChordButton, getnote
import ulab.numpy as np
import board

# Standard guitar tuning: E2–A2–D3–G3–B3–E4
OPEN_NAMES = ["E2","A2","D3","G3","B3","E4"]
OPEN_NOTES = [getnote(name) for name in OPEN_NAMES]


### RELATIVE CHORDS (based on frets)
x = -9999

# Basic chords: https://www.libertyparkmusic.com/read-guitar-chord-diagrams/
A = [x,0,2,2,2,0]
C = [x,3,2,0,1,0] # Note that numbers denote fret #, not finger #
D = [x,x,0,2,3,2]
E = [0,2,2,1,0,0]
F = [x,3,3,2,1,x]
G = [3,2,0,0,3,3]
Am = [x,0,2,2,1,0]
Dm = [x,x,0,2,3,1]
Em = [0,2,2,0,0,0]

# Advanced chords
# https://truefire.com/guitar-chord-charts/
# Dominant 7 guitar chords
A7 = [x,0,2,2,2,3]
B7 = [x,2,1,2,0,2]
C7 = [x,3,2,3,1,0]
D7 = [x,x,0,2,1,2]
E7 = [0,2,2,1,3,0]
F7 = [1,3,1,2,1,1]
G7 = [3,2,0,0,0,1]

# More minor chords
Bm = [x,2,4,4,3,2]
Cm = [x,3,5,5,4,3]
Fm = [1,3,3,1,1,1]
Gm = [3,5,5,3,3,3]

# More major chords
B = [x,2,4,4,4,2]

def shift_notes(notes, shifts):
    """ Shift a list of notes by a number of half-steps """
    # TODO: Check assertions
    shifted_notes = np.array(notes, dtype=np.int16) + np.array(shifts, dtype=np.int16) # Add the shift in note onto the note itself
    return shifted_notes
    
if __name__ == "__main__":
    print("OPEN_NOTES (midi numbers for an open chord): {}".format(OPEN_NOTES))
    
    # Phototransistor pins for strings (low-note strings first)
    STRINGS = [
        LightString(pin=board.GP10, note=OPEN_NOTES[0]),
        LightString(pin=board.GP11, note=OPEN_NOTES[1]),
        LightString(pin=board.GP12, note=OPEN_NOTES[2]),
        LightString(pin=board.GP13, note=OPEN_NOTES[3]),
        LightString(pin=board.GP14, note=OPEN_NOTES[4]),
        LightString(pin=board.GP15, note=OPEN_NOTES[5]),
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
    myguitar = LightInstrument(strings=STRINGS, chord_btns=CHORD_BTNS, beam_pin=board.GP2, midi_program=1)
    myguitar.run()
