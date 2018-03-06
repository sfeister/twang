# Test of the lasers, useful in troubleshooting harp problems
# Written by Scott Feister
#
# Documentation on initializing LED:
#   https://gpiozero.readthedocs.io/en/latest/recipes.html

from time import sleep
from gpiozero import LED

## INITIALIZE THE LASERS
LAS = 23 # Pin on which laser circuit is relayed
lasers = LED(LAS) # Initialize the laser as LED-style digital I/O

# DO A LASER ON/OFF DANCE
print("Flashing lasers three times.")

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

print("Test complete!")