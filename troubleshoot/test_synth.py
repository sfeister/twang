# Synthesizer sound test to be run as troubleshooting for the laser harp
# Tests the interplay of JACK and fluidsynth, with Python
#
# Written by Scott Feister
#
# Python script for catching Ctrl + C copied from https://www.devdungeon.com/content/python-catch-sigint-ctrl-c

from signal import signal, SIGINT
import subprocess
from sys import exit
from time import sleep
import jack # sudo apt install jackd python3-jack-client
import fluidsynth # sudo apt install fluidsynth; sudo pip3 install pyFluidSynth

def handler(signal_received, frame):
    # Handle any cleanup here
    print('SIGINT or CTRL-C detected. Exiting gracefully.')
    fs.delete()
    exit(0)

def jack_connect():
    """ Within JACK, connect fluidsynth ports to system playback ports (enabling sound from speakers) """
    client = jack.Client("MyGreatClient")

    # Identify the system and fluidsynth audio ports
    sysports = client.get_ports('system*', is_audio=True, is_output=False, is_physical=True)
    fluidports = client.get_ports('fluidsynth*', is_audio=True, is_output=True)

    if len(sysports) < 2:
        raise Exception("Found fewer than two system audio playback ports. Should have found one left channel and one right channel.")
    if len(fluidports) < 2:
        raise Exception("Found fewer than two fluidsynth audio output ports. Should have found one left channel and one right channel.")

    # Connect the fluidsynth ports to the system playback ports
    client.connect(fluidports[0], sysports[0]) # connect left port
    client.connect(fluidports[1], sysports[1]) # connect right port

    client.close()
    
if __name__ == '__main__':
    # Tell Python to run the handler() function when SIGINT (Ctrl + C) is recieved
    signal(SIGINT, handler)
    
    # Start fluidsynth (with jack)
    fs = fluidsynth.Synth()
    fs.start(driver="jack")

    sfid = fs.sfload("/usr/share/sounds/sf2/FluidR3_GM.sf2")
    fs.program_select(0, sfid, 0, 0)

    # Make the JACK audio connections to enable fluidsynth sound from speakers
    jack_connect()
    
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
