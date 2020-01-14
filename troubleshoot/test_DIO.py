# Test of the phototransistor on GPIO Pin #20, using state polling
# Written by Scott Feister
#
# Documentation on initializing Button:
#   https://gpiozero.readthedocs.io/en/latest/recipes.html

from time import sleep
from gpiozero import Button

################## INITIALIZATION ###########################
def callback1():
    """ Button callback function, prints a message to the terminal """
    print("Button pressed!!")
    
## INITIALIZE THE BUTTON
BTN = 20
button = Button(BTN)
button.when_pressed = callback1

## LISTEN FOR THE BUTTON PRESS
print("Press the button as many times as desired (message will display each time). Type Ctrl + C to stop.")
# Begin an infinite loop (keeps the script running, and listening for button presses)
while True:
    sleep(0.1) # This 'sleep' call prevents the infinite loop from hogging all of your system resources
