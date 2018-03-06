# Test of the lasers, combined with the button press
# Written by Scott Feister
#
# Documentation on initializing LED, Button:
#   https://gpiozero.readthedocs.io/en/latest/recipes.html

from time import sleep
from gpiozero import LED, Button

## INITIALIZE THE LASERS
LAS = 23 # Pin on which laser circuit is relayed
lasers = LED(LAS) # Initialize the laser as LED-style digital I/O

## INITIALIZE THE BUTTON
BTN = 24
button = Button(BTN)
button.when_pressed = lasers.on # When button is held down, turn on the lasers
button.when_released = lasers.off # When button is released, turn off the lasers

print("Press and hold button to turn on lasers; release button to turn them off.")
print("Type Ctrl + C when you are finished testing.")

## LISTEN FOR THE BUTTON PRESS
# Begin an infinite loop (keeps the script running, and listening for button presses)
while True:
    sleep(0.1) # This 'sleep' call prevents the infinite loop from hogging all of your system resources
