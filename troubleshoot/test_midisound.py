# Midi sound test to be run as troubleshooting for the laser harp
# Written by Scott Feister
#
# Before running:
#   1. Start the software synthesizer via command "startsynth"
#
# Python script for catching Ctrl + C copied from https://www.devdungeon.com/content/python-catch-sigint-ctrl-c

from signal import signal, SIGINT
from sys import exit
from time import sleep
import pygame.midi

def handler(signal_received, frame):
    # Handle any cleanup here
    print('SIGINT or CTRL-C detected. Exiting gracefully.')
    pygame.midi.quit()
    exit(0)
    
if __name__ == '__main__':
    # Tell Python to run the handler() function when SIGINT (Ctrl + C) is recieved
    signal(SIGINT, handler)# Start Pygame MIDI engine and set instrument output
    
    # Initialize MIDI player
    pygame.midi.init()
    player = pygame.midi.Output(0)
    player.set_instrument(0)

    print("Playing twelve notes in a row, using MIDI! You should hear them.")
    print("Press Ctrl + C to quit early.")
    # 12 and 19 are fine instruments
    for i in range(12):
        player.note_on(60+i, 127)
        sleep(0.3)
        player.note_off(60+i, 127)
        sleep(0.05)
        
    for i in range(11):
        player.note_on(60+i, 127)
        sleep(0.05)
        player.note_off(60+i, 127)
        sleep(0.01)

    player.note_on(60+11, 127)
    sleep(3)
    player.note_off(60+11, 127)
    sleep(0.5)
        
    pygame.midi.quit()