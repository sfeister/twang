# twang
Python library for a middle school Raspberry Pi Laser Harp (built with a CNC and Raspberry Pi Zero).

More generally, this Python library could be adapted for any beambreak-based instrument built using the Raspberry Pi. Feel free to send me an email if you'd like help making an adaptation!

This Python code goes along with a middle school project to create a harp where the strings are laser beams. Goals of this wider project are learning about circuits, CAD, and computer programming. See our project page on Hackaday: https://hackaday.io/project/28159

The scripts are meant to be run in Python2.7+. They were tested on Raspberry Pi 3 with the "Raspbian Jessie" operating system.

## Installing dependencies
This toolkit has software dependencies:
* jackd (JACK Audio Connection Kit - http://www.jackaudio.org/)

It also has python package dependencies:
* adafruit-mcp3008 (https://github.com/adafruit/Adafruit_Python_MCP3008)
* pyo

Together, JACK and pyo enable low-latency audio mixing for playing the sounds of "plucked" harp strings. The adafruit-mcp3008 library enables us to read analog voltage values using an MCP3008 chip (the Pi natively only has digital I/O): useful for noticing a change to photoresistors when the laser beam is blocked.

These dependencies, and a few others, can be installed onto your Raspberry Pi (Raspbian Jessie) as follows:

1. First, update your Raspbian Jessie package repositories:
```
sudo apt update
```

2. Next, install all the dependencies via:
```
sudo apt install jackd python-pyo python-pip python-numpy python-gpiozero
sudo pip install adafruit-mcp3008
```

## Downloading this library
Download and unzip all files in this repository into a local directory.

## Running the harp
1. Check you have audio output working with your speakers. Test this by trying to play a sound file in a standard Raspbian sound player, like Audacity. If you don't hear sound, you can change between HDMI audio, analog audio, and other audio output options by left-clicking the volume icon found in the upper right corner of the Raspbian desktop.

2. If you are running your Pi with a display (connected to a monitor or TV), you can skip to the next step. If you are running without a display (no monitor, e.g. logging in via ssh), run, from the command line:
```export DISPLAY=:0```

3. Next, start the JACK audio server from the command line:
```jackd -d alsa -n 16 &```

4. Once the JACK server is started, navigate into the source directory and run:
```python laserharp.py ```

## Troubleshooting the harp
Rather than jumping right to laserharp.py, it is very useful to run the "test_[something].py" scripts when building and troubleshooting the laser harp. The "test_debugger.py" script is especially helpful. Run this script by:
``` python test_debugger.py ```
You will still need to check audio output and start the JACK server before running any tests involving audio (follow steps 1 - 3 of the previous section).

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

## Circuit diagrams
You will need to build certain circuits before running the Python scripts; for example, you can't test the calibration button if it's not wired to the Pi Zero! Circuit and connections diagrams for the five-string laser harp are available, as a PDF, in the "diagrams" directory. You can follow these diagrams to construct the physical circuits that go along with this Python code.

The diagrams were made using the free, open-source vector graphics software [Inkscape](https://www.audacityteam.org/). Vector graphics (.svg format) for circuit elements, warning symbols, and more were gathered from [Wikimedia Commons] (https://commons.wikimedia.org) and incorporated into the laser harp diagrams. I found this [collection of electrical symbols](https://commons.wikimedia.org/wiki/File:Electrical_symbols_library.svg) particularly helpful.

## Physical construction
To physically build the five-string laser harp, you should follow instructions on [our Hackaday project page](https://hackaday.io/project/28159). As of Spring 2018, we are in the process of writing our instructions, so stay 'tuned'!

## Sound samples
Audio samples included in this repository were downloaded from the Philharmonia Orchestra, then snipped and amplified in the free, open-source [Audacity audio editor](https://www.audacityteam.org/).

More freely useable sound samples are available at:
http://www.philharmonia.co.uk/explore/sound_samples
