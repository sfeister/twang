# Midi-based sound test to be run as troubleshooting for the laser harp
# Written by Scott Feister
#
# Python script for catching Ctrl + C copied from https://www.devdungeon.com/content/python-catch-sigint-ctrl-c

from signal import signal, SIGINT
import subprocess
from sys import exit
from time import sleep
import fluidsynth # sudo apt install fluidsynth; sudo pip3 install pyFluidSynth

def handler(signal_received, frame):
    # Handle any cleanup here
    print('SIGINT or CTRL-C detected. Exiting gracefully.')
    fs.delete()
    exit(0)
    
if __name__ == '__main__':
    # Tell Python to run the handler() function when SIGINT (Ctrl + C) is recieved
    signal(SIGINT, handler)
    
    # Start fluidsynth (with jack)
    fs = fluidsynth.Synth()
    fs.start(driver="jack")

    sfid = fs.sfload("/usr/share/sounds/sf2/FluidR3_GM.sf2")
    fs.program_select(0, sfid, 0, 0)

    # Make the jack audio connections of fluidsynth outputs to enable system playback
    subprocess.call(["jack_connect", "fluidsynth:l_00", "system:playback_1"])
    subprocess.call(["jack_connect", "fluidsynth:r_00", "system:playback_2"])

    print("Playing twelve notes in a row, using MIDI! You should hear them.")
    print("Press Ctrl + C to quit early.")
    # 12 and 19 are fine instruments
    for i in range(12):
        fs.noteon(0, 60+i, vel=127)
        sleep(0.3)
        fs.noteoff(0, 60+i)
        sleep(0.05)
        
    for i in range(11):
        fs.noteon(0, 60+i, vel=127)
        sleep(0.05)
        fs.noteoff(0, 60+i)
        sleep(0.01)

    fs.noteon(0, 60+11, vel=127)
    sleep(3)
    fs.noteoff(0, 60+11)
    sleep(0.5)

    fs.delete()
