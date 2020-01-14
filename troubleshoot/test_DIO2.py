# Test of the phototransistor on GPIO Pin #20, using interrupts
# Written by Scott Feister
#
# Documentation on initializing Button:
#   https://raspberrypihq.com/use-a-push-button-with-raspberry-pi-gpio/

from signal import signal, SIGINT
from sys import exit
from time import sleep
import RPi.GPIO as GPIO

def handler(signal_received, frame):
    # Handle any cleanup here
    print('SIGINT or CTRL-C detected. Exiting gracefully.')
    GPIO.cleanup()
    exit(0)
    
def callback1(channel):
    """ Button callback function, prints a message to the terminal """
    print("Button pressed!!")
    
if __name__ == '__main__':
    # Tell Python to run the handler() function when SIGINT (Ctrl + C) is recieved
    signal(SIGINT, handler)

    ## INITIALIZE THE BUTTON
    BTN = 20
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BTN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(BTN, GPIO.FALLING, callback=callback1, bouncetime=100)
    print("Press the button as many times as desired (message will display each time). Type Ctrl + C to stop.")
    while True:
        sleep(5)