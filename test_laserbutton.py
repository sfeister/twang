# Test of the lasers, combined with the button press
# Written by Scott Feister
#
# Documentation on initializing LED, Button:
#   https://gpiozero.readthedocs.io/en/latest/recipes.html

from time import sleep
from gpiozero import LED, Button

############### TEST 1: Lasers Only #################

## INITIALIZE THE LASERS
LAS = 23 # Pin on which laser circuit is relayed
lasers = LED(LAS) # Initialize the laser as LED-style digital I/O

# DO A LASER ON/OFF DANCE
print("Test 1 of 2: Flashing lasers three times.")
lasers.on()
sleep(0.25)
lasers.off()
sleep(0.25)
lasers.on()
sleep(0.25)
lasers.off()
sleep(0.25)
lasers.on()
sleep(0.25)
lasers.off()
sleep(0.25)

############### TEST 2: Lasers + Button #################

## INITIALIZE THE BUTTON
BTN = 24
button = Button(BTN)
button.when_pressed = lasers.on # When button is held down, turn on the lasers
button.when_released = lasers.off # When button is released, turn off the lasers

print("Test 2 of 2: Press button to turn on lasers; release button to turn them off.")
print("Type Ctrl + C when you are finished testing.")

## LISTEN FOR THE BUTTON PRESS
# Begin an infinite loop (keeps the script running, and listening for button presses)
while True:
    sleep(0.1) # This 'sleep' call prevents the infinite loop from hogging all of your system resources