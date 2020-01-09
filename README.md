# twang
Python library for a middle school Raspberry Pi Laser Harp and/or Laser Guitar (built with a CNC and Raspberry Pi Zero).

More generally, this Python library could be adapted for any beambreak-based instrument built using the Raspberry Pi. Feel free to send me an email if you'd like help making an adaptation!

The Python scripts go along with a middle school project to create a harp where the strings are laser beams. Goals of this wider project are learning about circuits, CAD, and computer programming. See our [Hackaday project page](https://hackaday.io/project/28159) for more details!

The scripts are meant to be run in Python3.7+. They were tested on the Raspberry Pi Zero W with the "Raspbian Stretch" operating system.

## Note to the Reader
The target audience for this README is *not* the middle school student, and not necessarily even the middle school teacher, but someone already familiar with installing packages on Linux systems. We will be giving our middle school students a microSD card with everything "ready to go". They won't need to figure out how to install all of the dependencies listed below! If you are a teacher and are having trouble following the instructions below, please reach out to me directly (Scott Feister), and I will be happy to share with you a microSD card image that has everything already installed.

## Physical pre-requisites
You will need to build certain circuits before running the Python scripts; for example, you can't test a button if it's not wired to the Raspberry Pi! Circuit and connections diagrams for the five-string laser harp are available, as a PDF, in the "diagrams" directory. You can follow these diagrams to construct the physical circuits that go along with this Python code.

For more information on the physical construction of the five-string laser harp we are using for the middle school project, you should follow instructions on our [Hackaday project page](https://hackaday.io/project/28159). As of Spring 2018, we are in the process of writing our instructions, so stay 'tuned'!

## Installing dependencies on the Raspberry Pi
This toolkit has software dependencies:
* jackd (JACK Audio Connection Kit - http://www.jackaudio.org/)
* fluidsynth

It also has Python package dependencies:
* adafruit-gpio
* gpiozero
* pygame
* numpy

And the following additional dependencies:
* fluid-soundfont-gs (or any "Soundfont" for playback of MIDI)

The adafruit-gpio and gpiozero Python libraries enables us to measure digital inputs on the Raspberry Pi: useful for noticing the fast change in signal from a phototransistor when the laser beam is blocked, and also useful for noticing when a button is pressed. The pygame Python library lets us generate MIDI signals representing musical notes. These MIDI signals are processed by JACK and fluidsynth (a 'software synthesizer'). Together, these enable low-latency audio mixing of the sounds of "plucked" harp strings on our external speakers.

These dependencies, and a few others, can be installed onto your Raspberry Pi (Raspbian Jessie) as follows:

1. First, update your Raspbian Jessie package repositories:
```
sudo apt update
```

2. Next, install all the dependencies via:
```
sudo apt install jackd fluidsynth python3-pip python3-numpy python3-gpiozero fluid-soundfont-gs
sudo pip3 install adafruit-gpio
```

You may also install these optional software for additional control and troubleshooting of your software synthesizer setup:
```
sudo apt install qsynth patchage qjackctl vmpk
```

Qsynth is a graphical interface for fluidsynth. Qjackctl is a graphical interface for JACK.  Patchage is a graphical interface for making software connections between various audio and MIDI components running in JACK. Vmpk is a software musical keyboard.

## Downloading this library
Download and unzip all files in this repository into a local directory on the Raspberry Pi.

## Running the harp
After physical construction of the laser harp:

1. Check you have audio output working with your speakers. Test this by trying to play a sound file in a standard Raspbian sound player, like Audacity. If you don't hear sound, you can change between HDMI audio, analog audio, and other audio output options by left-clicking the volume icon found in the upper right corner of the Raspbian desktop.

2. If you are running your Pi with a display (connected to a monitor or TV), you can skip to the next step. If you are running without a display (no monitor, e.g. logging in via ssh), run, from the command line:
```export DISPLAY=:0```

3. Next, start the JACK audio server from the command line:
```jackd -d alsa -n 16 &```

4. Once the JACK server is started, navigate into the source directory and run:
```python laserharp.py ```

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
``` python test_debugger.py ```
You will still need to check audio output and start the JACK server before running any tests involving audio (follow steps 1 - 3 of the previous section).

## Credits
This project was created by Alex Wulff (DeAnza Academy of Technology and the Arts), Scott Feister (California State University Channel Islands), and Phil Hampton (California State University Channel Islands). We originally designed, built, and interactively displayed the five-string laser harp for K-8 children at the [CSUCI Annual Science Carnival](https://www.csuci.edu/sciencecarnival/) in November 2017. It was a big hit, so we have decided to develop it into a middle school project!

### Sound samples
Audio samples included in this repository were downloaded from the Philharmonia Orchestra, then snipped and amplified in the free, open-source [Audacity audio editor](https://www.audacityteam.org/). Each note is exported as a .wav file and saved in the "sounds" directory.

More freely useable sound samples are available at:
http://www.philharmonia.co.uk/explore/sound_samples

### Circuit diagrams
We made the laser harp circuit diagrams using the free, open-source vector graphics software [Inkscape](https://www.audacityteam.org/). Vector graphics (*.svg* format) for circuit elements, warning symbols, and more were gathered from [Wikimedia Commons](https://commons.wikimedia.org) and incorporated into the laser harp diagrams. I found this [collection of electrical symbols](https://commons.wikimedia.org/wiki/File:Electrical_symbols_library.svg) and this [laser warning symbol](https://commons.wikimedia.org/wiki/File:Laser-symbol.svg) particularly helpful.

