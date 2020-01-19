# NOTE: You are on the legacy2018 branch, which is not the most up-to-date.
As of January 2020, this entire branch ("legacy2018") of the repository involving the MCP3008 and analog inputs for the five-string guitar is depreciated, in favor of a new approach with phototransistors and digital inputs.

However, if you'd like to create the original harp design from 2017, you are in the right place!

# twang
Python library for a middle school Raspberry Pi Laser Harp (built with a CNC and Raspberry Pi Zero).

More generally, this Python library could be adapted for any beambreak-based instrument built using the Raspberry Pi. Feel free to send me an email if you'd like help making an adaptation!

The Python scripts go along with a middle school project to create a harp where the strings are laser beams. Goals of this wider project are learning about circuits, CAD, and computer programming. See our [Hackaday project page](https://hackaday.io/project/28159) for more details!

The scripts were designed to be run in Python2.7+, but I have been testing them with Python3.6+ as well. They were tested on Raspberry Pi 3 and Raspberry Pi Zero W with the "Raspbian Stretch" operating system, but I have been testing them with "Raspbian Buster" as well.

## Physical pre-requisites
You will need to build certain circuits before running the Python scripts; for example, you can't test a button if it's not wired to the Raspberry Pi! Circuit and connections diagrams for the five-string laser harp are available, as a PDF, in the "diagrams" directory. You can follow these diagrams to construct the physical circuits that go along with this Python code.

For more information on the physical construction of the five-string laser harp we are using for the middle school project, you should follow instructions on our [Hackaday project page](https://hackaday.io/project/28159). As of January 2020, this entire branch ("legacy2018") of the repository involving the MCP3008 and analog inputs for the five-string guitar is depreciated, in favor of a new approach with phototransistors and digital inputs.

## Installing dependencies on the Raspberry Pi
This toolkit has Python package dependencies:
* adafruit-mcp3008 (https://github.com/adafruit/Adafruit_Python_MCP3008)
* pygame

Pygame enables audio mixing for playing the sounds of "plucked" harp strings. The adafruit-mcp3008 library enables us to read analog voltage values using an MCP3008 chip (the Raspberry Pi natively only has digital I/O): useful for noticing a change to photoresistors when the laser beam is blocked.

These dependencies, and a few others, can be installed onto your Raspberry Pi (Raspbian Jessie) as follows:

1. First, update your Raspbian package repositories:
```
sudo apt update
```

2. (Python2) If you want to use Python2, install all the dependencies for Python2.7+ via:
```
sudo apt install python-pygame python-pip python-numpy python-gpiozero
sudo pip install git+https://github.com/adafruit/Adafruit_Python_MCP3008.git
```

2. (Python3) Alternatively, if you want to use Python3, install all the dependencies for Python3.6+ via:
```
sudo apt install python3-pygame python3-pip python3-numpy python3-gpiozero
sudo pip3 install git+https://github.com/adafruit/Adafruit_Python_MCP3008.git
```

## Downloading this library
Download and unzip all files in this repository into a local directory on the Raspberry Pi.

## Running the harp
After physical construction of the laser harp:

1. Check you have audio output working with your speakers. Test this by trying to play a sound file in a standard Raspbian sound player, like Audacity. If you don't hear sound, you can change between HDMI audio, analog audio, and other audio output options by left-clicking the volume icon found in the upper right corner of the Raspbian desktop.

2. (Python2) Navigate into the source directory and run ```python laserharp.py ```, or (Python3) Navigate into the source directory and run ```python laserharp.py```

## Troubleshooting the harp
Several Python scripts for testing and running the five-string laser harp are included:

Python script | Action
--- | ---
test_button.py | Waits for physical button press
test_lasers.py | Flashes the lasers three times
test_ADC.py | Reads and displays values from the MCP3008 analog-to-digital converter (ADC)
test_sound.py | Plays harp sounds, testing the audio mixer
test_laserbutton.py | Combined test of the lasers and physical button
test_calibrate.py | Combined test of on/off laser calibration (checking quality of physical beam break)
test_debugger.py | Combined test intended for comprehensive debugging
laserharp.py | Runs the laser harp as a playable instrument

Rather than jumping right to laserharp.py, it is very useful to run the "test_[something].py" scripts when building and troubleshooting the laser harp. The "test_debugger.py" script is especially helpful. Run this script by:
``` python test_debugger.py ``` (Python2), or
``` python3 test_debugger.py ``` (Python3)
You will still want to generally check audio output before running any tests involving audio (follow step 1 of the previous section).

## Credits
This project was created by Alex Wulff (DeAnza Academy of Technology and the Arts), Scott Feister (University of Chicago), and Phil Hampton (California State University Channel Islands). We originally designed, built, and interactively displayed the five-string laser harp for K-8 children at the [CSUCI Annual Science Carnival](https://www.csuci.edu/sciencecarnival/) in November 2017. It was a big hit, so we have decided to develop it into a middle school project!

### Sound samples
Audio samples included in this repository were downloaded from the Philharmonia Orchestra, then snipped and amplified in the free, open-source [Audacity audio editor](https://www.audacityteam.org/). Each note is exported as a .wav file and saved in the "sounds" directory.

More freely useable sound samples are available at:
http://www.philharmonia.co.uk/explore/sound_samples

### Circuit diagrams
We made the laser harp circuit diagrams using the free, open-source vector graphics software [Inkscape](https://www.audacityteam.org/). Vector graphics (*.svg* format) for circuit elements, warning symbols, and more were gathered from [Wikimedia Commons](https://commons.wikimedia.org) and incorporated into the laser harp diagrams. I found this [collection of electrical symbols](https://commons.wikimedia.org/wiki/File:Electrical_symbols_library.svg) and this [laser warning symbol](https://commons.wikimedia.org/wiki/File:Laser-symbol.svg) particularly helpful.

