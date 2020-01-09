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
s = pyo.Server(duplex=0, audio='jack').boot() # Boot the pyo server
s.setJackAuto(False, False)
s.start()

nstrings = 5 # Number of harp strings
scriptdir = os.path.dirname(os.path.realpath(__file__)) # Directory of this script
notedir = os.path.join(scriptdir, "sounds", "guitar") # Directory containing list of audio files
#notedir = r"/home/pi/mycode/twang/sounds/guitar" # Directory containing list of audio files
notes = ["c4", "d4", "e4", "f4", "g4"]  # List of wav files in the notedir folder
ext = ".wav"

sounds = [None]*nstrings

for i in range(nstrings):
    sounds[i] = pyo.SfPlayer(os.path.join(notedir, notes[i] + ext))

## PLAY SOME NOTES
print("Playing lovely sounds. Press Ctrl + C to quit.")
# Play each of the notes in sequence
for i in range(nstrings):
    sounds[i].out() # Play the ith harp note
    sleep(0.25) # Wait a quarter second

sleep(1.5) # Wait a second and a half

# Play the low note five times in a row (testing for sound blend)
for i in range(5):
    sounds[0].out() # Play the lowest harp note
    sleep(0.25) # Wait a quarter second

sleep(2) # Allow the final note some time to die off before closing program

print("Sound test complete!")
