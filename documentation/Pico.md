# Programming Your Pi Pico

By Dr. Scott Feister

Updated March 5, 2025

In this guide, I will go through how to program your Pi Pico to turn it into a MIDI instrument.

## Write Python and Troubleshoot Your Instrument

##### Parts needed:

* Pi Pico

* Your fully constructed circuits, wired into the Pi Pico

* A laptop / chromebook

##### At the end of this section you should:

* Have a working light instrument!


### First Setup of Pi Pico

1. [Follow all of these steps first to install CircuitPython 9.x on your Pi.](https://learn.adafruit.com/getting-started-with-raspberry-pi-pico-circuitpython/circuitpython)
    a. After following these steps, your Pi Pico will show up on your laptop as a USB flash drive called "CIRCUITPY". Proceed!
2. Open up the "CIRCUITPY" drive, and navigate to the "lib" folder. It's empty, but we are going to add some folders here next.
3. Download the [CircuitPython Bundle for Version 9.x] (https://circuitpython.org/libraries) and unzip it. From inside what you downloaded, navigate to the "lib" folder.
4. From the CircuitPython Bundle for Version 9.x "lib" folder, copy a folder called "adafruit_midi" into your CIRCUITPY "lib" folder.
5. Download the latest [Twang GitHub Repository] (https://github.com/sfeister/twang/archive/refs/heads/main.zip) and unzip it.
6. From inside the Twang GitHub Reposotory "twang-main" folder you downloaded, copy the folder called "twang" into your CIRCUITPY "lib" folder.

#### Editing code.py
1. You'll do all your editing on the CIRCUITPY USB drive "code.py" file.
1. From inside the Twang GitHub Reposotory "twang-main" folder you downloaded, explore the examples inside the "examples" folder. Any of these can be copied to overwrite "code.py."
1. For example, you can copy the contents of "guitar.py" and overwrite the contents of "code.py". Or, you can copy the contents of "harp.py" and overwrite the contents of "code.py".

#### Troubleshooting
1. Troubleshoot using the Serial Editor first.
2. Then, troubleshoot using something like [MidiMonitor](https://www.midimonitor.com/) or [DotPiano](https://dotpiano.com/) in Google Chrome.




#### Customization
While I won't spell out the details here, this is where you write your Python code that runs your instrument! For example, you could use the example of the six-string/four-chord-button guitar in the twang repository: "examples/guitar.py".

Start with one of the example files like "harp.py", then copy it somewhere else, rename it, and edit it to make your own instrument.

When you feel great about everything, it's time to reboot and test. Unplug and replug your Pi Pico, and wait for the lasers to turn on. Is everything working as an instrument should? If not, talk with your teacher for more help troubleshooting.