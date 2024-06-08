#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
harp.py: One-string laser harp with MIDI output

Start your instrument via "python3 harp.py"

Notes:
 * Valid pins are, in left-to-right order along the Pi Stereo Bonnet: 4,17,27,22,25,5,6,12,13,16,20
     ** (Reverse order: 20,16,13,12,6,5,25,22,27,17,4)
 * The MIDI note codes for nine notes in a major scale (C to C) are: 60,62,64,65,67,69,71,72,73

Created by Scott Feister on June 8, 2024
"""

from twang import LightString, LightInstrument

if __name__ == "__main__":
    ## Define your ten strings (low-note strings first)
    lstrings = [None]*1
    lstrings[0] = LightString(pin=16, midinote=60)
    
    ## Combine the strings together into a playable instrument!
    myharp = LightInstrument(lstrings, midi_instrument=8, gain=1.0)
    myharp.start()