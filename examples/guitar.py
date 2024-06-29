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
opennames = ["E2","A2","D3","G3","B3","E4"]
opennotes = [getnote(name) for name in opennames]


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

def midify(relnotes):
    """ Convert relative chord to an absolute chord in midi
    Relies on variables opennotes and x defined above"""
    notes = np.array(relnotes, dtype=np.int16) + np.array(opennotes, dtype=np.int16)
    notes[notes < 0] = -9999 # Reset unpluckable strings to -9999
    return notes
    
if __name__ == "__main__":
    # Button pins for chords, and their associated chords
    cbuttons = [None]*4
    cbuttons[0] = ChordButton(pin=board.GP20, midinotes=midify(C))
    cbuttons[1] = ChordButton(pin=board.GP21, midinotes=midify(G))
    cbuttons[2] = ChordButton(pin=board.GP22, midinotes=midify(Am))
    cbuttons[3] = ChordButton(pin=board.GP23, midinotes=midify(F))
    
    # Phototransistor pins for strings (low-note strings first)
    lstrings = [None]*6
    lstrings[0] = LightString(pin=board.GP11, midinote=opennotes[0])
    lstrings[1] = LightString(pin=board.GP12, midinote=opennotes[1])
    lstrings[2] = LightString(pin=board.GP13, midinote=opennotes[2])
    lstrings[3] = LightString(pin=board.GP14, midinote=opennotes[3])
    lstrings[4] = LightString(pin=board.GP15, midinote=opennotes[4])
    lstrings[5] = LightString(pin=board.GP16, midinote=opennotes[5])
    
    # Combine the buttons and strings together into an instrument!
    myguitar = LightInstrument(lstrings, chordbtns=cbuttons, beampin=board.GP2)
    myguitar.run()
