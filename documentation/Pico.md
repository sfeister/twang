# Programming Your Pi Pico

By Dr. Scott Feister

Updated March 20, 2025

In this guide, I will go through how to program your Pi Pico to turn it into a MIDI instrument.

## Write Python and Troubleshoot Your Instrument

##### Parts needed:

* Pi Pico

* A laptop / chromebook

* USB A to USB micro cable (to plug your Pi Pico into your laptop)

##### At the end of this section you should:

* Have a Pi Pico with "twang" instrument firmware running on it


### Flash CircuitPython (not MicroPython) to Your Pico

Follow all the steps at this page: [Install CircuitPython 9.x on your Pi.](https://learn.adafruit.com/getting-started-with-raspberry-pi-pico-circuitpython/circuitpython)
 
After following these steps, your Pi Pico will show up on your laptop as a USB flash drive called "CIRCUITPY".

If you can see your USB flash drive and it's called "CIRCUITPY" now, proceed! Otherwise, check that you've completed all steps in the hyperlink above.

### Add the "adafruit_midi" CircuitPython library to your Pico

You'll now add a library called "adafruit_midi" to your Pico. This library lets us send MIDI messages, which are important for our virtual instrument to work right.

Follow these steps to add "adafruit_midi" to your Pico.
1. Plug in your Pico to your laptop. It should show up as as USB flash drive called "CIRCUITPY". (If it doesn't, double check your earlier steps in earlier sections).
1. On your laptop, download the latest [CircuitPython Bundle for Version 9.x] (https://circuitpython.org/libraries). (Download the "Bundle", not the "Community Bundle".) For example, on March 7, 2025, I downloaded "adafruit-circuitpython-bundle-9.x-mpy-20250307.zip".
1. Unzip the folder.
1. From the folder you unzipped, navigate to the "lib" folder.
1. Inside of your CIRCUITPY USB drive, there should *also* be a folder called "lib". 
1. Copy the folder called "adafruit_midi" from the unzipped "lib" folder into your CIRCUITPY USB drive's "lib" folder. (If you don't see a folder called "adafruit_midi" in your unzipped "lib" folder, you might have accidentally downloaded the wrong CircuitPython Bundle. Double check your steps above.)

You should now have a folder called "adafruit_midi" inside of your CIRCUITPY/lib/ folder. If so, you're ready to move onto the next step.

### Add the "twang" CircuitPython library to your Pico

1. Plug in your Pico to your laptop. It should show up as as USB flash drive called "CIRCUITPY". (If it doesn't, double check your earlier steps in earlier sections).
1. On your laptop, download the latest [Twang GitHub Repository] (https://github.com/sfeister/twang/archive/refs/heads/main.zip).
1. Unzip the folder.
1. From inside the folder you just unzipped, there should be a folder called "twang-main". Open up the "twang-main" folder. Inside, there's a folder called "twang".
1. Inside of CIRCUITPY, there should be a folder called "lib". 
1. Copy the folder called "twang" into your CIRCUITPY USB drive's "lib" folder.

You should now have a folder called "twang" inside of your CIRCUITPY/lib/ folder, right next to your "adafruit_midi" folder. If so, you're ready to move onto the next step.

#### Edit code.py

1. Plug in your Pico to your laptop. It should show up as as USB flash drive called "CIRCUITPY". (If it doesn't, double check your earlier steps in earlier sections).
1. Inside of CIRCUITPY, there should be a file called "code.py".
1. This file, "code.py", is the Python code that will run whenever you use the Pico.
1. From inside the Twang GitHub Reposotory "twang-main" folder you downloaded in an earlier step, there is a folder called "examples". Open up the "examples" folder.
1. The contents of any of these example files can be copied to overwrite "code.py."
1. For example, you can copy the contents of "guitar.py" and overwrite the contents of "code.py". Or, you can copy the contents of "harp.py" and overwrite the contents of "code.py".
1. For now, copy the contents of "guitar.py" to overwrite "code.py".

#### Troubleshooting
1. Troubleshoot using the Serial Editor first.
2. Then, troubleshoot using something like [MidiMonitor](https://www.midimonitor.com/) or [DotPiano](https://dotpiano.com/) in Google Chrome.




#### Customization
While I won't spell out the details here, this is where you write your Python code that runs your instrument! For example, you could use the example of the six-string/four-chord-button guitar in the twang repository: "examples/guitar.py".

Start with one of the example files like "harp.py", then copy it somewhere else, rename it, and edit it to make your own instrument.

When you feel great about everything, it's time to reboot and test. Unplug and replug your Pi Pico, and wait for the lasers to turn on. Is everything working as an instrument should? If not, talk with your teacher for more help troubleshooting.