# Sound test to be run as troubleshooting for the laser harp
# Written by Scott Feister
#
# Start jack before running this script, e.g. via
#   export DISPLAY=:0 
#   jackd -d alsa -n 16 &
# 

import os
from time import sleep
from datetime import datetime
import numpy as np
import pyo

## INITIALIZE THE SOUND MIXER
s = pyo.Server(duplex=0).boot() # Boot the pyo server
s.start()

nstrings = 5 # Number of harp strings

notedir = r"/home/pi/mycode/harp/sounds/guitarwav" # Directory containing list of audio files
notes = ["c4", "d4", "e4", "f4", "g4", "a4", "b4"] # Should be equal to or longer in length than number of strings
ext = ".wav"

sounds = [None]*nstrings

for i in range(nstrings):
    sounds[i] = pyo.SfPlayer(os.path.join(notedir, notes[i] + ext))

## PLAY SOME NOTES

# Play each of the notes in sequence
for i in range(nstrings):
    sounds[i].out() # Play the ith harp note
    sleep(0.25) # Wait a quarter second

sleep(1.5) # Wait a second and a half

# Play the low note five times in a row (testing for sound blend)
for i in range(5):
    sounds[0].out() # Play the lowest harp note
    sleep(0.25) # Wait a quarter second
