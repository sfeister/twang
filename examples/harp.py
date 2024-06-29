#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
harp.py: Ten-string laser harp with MIDI output, for Pi Pico

Notes:
 * The MIDI note codes for nine notes in a major scale (C to C) are: 60,62,64,65,67,69,71,72,73

Created by Scott Feister on June 28, 2024
"""

from twang import LightString, LightInstrument
import board

if __name__ == "__main__":
    ## Define your ten strings (low-note strings first)
    lstrings = [None]*10
    lstrings[0] = LightString(pin=board.GP10, midinote=60)
    lstrings[1] = LightString(pin=board.GP11, midinote=62)
    lstrings[2] = LightString(pin=board.GP12, midinote=64)
    lstrings[3] = LightString(pin=board.GP13, midinote=65)
    lstrings[4] = LightString(pin=board.GP14, midinote=67)
    lstrings[5] = LightString(pin=board.GP15, midinote=69)
    lstrings[6] = LightString(pin=board.GP16, midinote=71)
    lstrings[7] = LightString(pin=board.GP17, midinote=72)
    lstrings[8] = LightString(pin=board.GP18, midinote=73)
    lstrings[9] = LightString(pin=board.GP19, midinote=75)
    
    ## Combine the strings together into a playable instrument!
    myharp = LightInstrument(lstrings, beampin=board.GP2)
    myharp.run()