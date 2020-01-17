#!/usr/bin/env python3

import subprocess
import RPi.GPIO as GPIO

LEDPIN = 23 # Our chosen LED pin to blink during shutdown (laser pin)
PWRBTN = 3 # FYI, Pin 3 on the Pi ships with a physical pull-up resistor attached

GPIO.setmode(GPIO.BCM)
GPIO.setup(PWRBTN, GPIO.IN)

GPIO.wait_for_edge(PWRBTN, GPIO.FALLING)

# Stop all synth and send shutdown command
print("Calling 'stopsynth'")
subprocess.call(['stopsynth'])
print("Executing shutdown -h now command")
subprocess.call(['shutdown', '-h', 'now'])

GPIO.cleanup() # Disable all previous GPIO settings
GPIO.setmode(GPIO.BCM)
GPIO.setup(LEDPIN, GPIO.OUT)

# Blink the LED wired to the our chosen LED pin
while True:
    GPIO.output(LEDPIN, 1) # Turn on 
    sleep(0.1)
    GPIO.output(LEDPIN, 0) # Turn off
    sleep(0.1)
