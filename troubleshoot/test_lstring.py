# Test of a single lightstring on GPIO Pin #20
# Written by Scott Feister
#
# Documentation on initializing Button:
#   https://raspberrypihq.com/use-a-push-button-with-raspberry-pi-gpio/

from signal import signal, SIGINT
from sys import exit
from time import sleep
import pygame.midi
import RPi.GPIO as GPIO
from twang import LightString

def handler(signal_received, frame):
    # Handle any cleanup here
    print('SIGINT or CTRL-C detected. Exiting gracefully.')
    GPIO.cleanup()
    pygame.midi.quit()
    exit(0)
    
if __name__ == '__main__':
    # Tell Python to run the handler() function when SIGINT (Ctrl + C) is recieved
    signal(SIGINT, handler)

    # Initialize MIDI player
    pygame.midi.init()
    player = pygame.midi.Output(0)
    player.set_instrument(0)

    ## INITIALIZE THE LIGHT STRING
    lstring = LightString(pin=20, midinote=60)

    print("Playing three plucks in a row, using MIDI! You should hear them.")
    print("Press Ctrl + C to quit early.")
    
    for i in range(3):
        lstring.play(player)
        sleep(1)

    print("Now, waiting for you to pluck the string, as many times as you want! Press Ctrl + C to quit.")
    lstring.start()
    while True:
        lstring.check_and_play(player)