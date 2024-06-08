from datetime import datetime
from signal import signal, SIGINT, SIGTERM
from sys import exit
import subprocess
from time import sleep
import numpy as np
import jack # sudo apt install jackd python3-jack-client
import jack_server
import fluidsynth # sudo apt install fluidsynth; sudo pip3 install pyFluidSynth
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

server = jack_server.Server(
    name="InstrumentServer",
    sync=True,
    realtime=False,
    driver="alsa",
    device="hw:MAX98357A",
    rate=48000,
    period=1024,
    # nperiods=2  # Work only with `alsa` driver
)

#print("Starting JACK server")
#server.start()

#print("Starting JACK client")
#client = jack.Client("MyGreatClient", no_start_server=True, servername="InstrumentServer")

# Start fluidsynth and set instrument output
print("Starting fluidsynth.")
fs = fluidsynth.Synth(samplerate=48000, gain=0.2, channels=256)
fs.start(driver="jack", device="hw:MAX98357A")
sfid = fs.sfload("/usr/share/sounds/sf2/Guitars-Universal-V1.5.sf2")
fs.program_select(0, sfid, 0, 0)

