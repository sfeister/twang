# twang

Python library for a middle school Raspberry Pi Laser Harp and/or Laser Guitar (built with a CNC and Raspberry Pi Zero).

More generally, this Python library could be adapted for any beambreak-based instrument built using the Raspberry Pi. Feel free to send me an email if you'd like help making an adaptation!

The Python scripts go along with a middle school project to create a harp where the strings are laser beams. Goals of this wider project are learning about circuits, CAD, and computer programming.

The scripts are meant to be run in Python3.6+. They were tested on the Raspberry Pi Zero W with the "Raspbian Buster" operating system.

## Note to the Reader

The target audience for this README is *not* the middle school student, and not necessarily even the middle school teacher, but someone already familiar with python packages on Linux systems, and who wants to understand this python package better. 

If you are a middle schooler, middle school teacher, or someone just interested in building an instrument, you can skip the rest of this page and instead follow directions from the following three pages (in order):

1. [Preparing your Raspberry Pi to be an Instrument](documentation/PreparingYourPi.md)

2. [Safe Design and Usage of a Laser Instrument](documentation/Safety.md)

3. [Building the Instrument Hardware](documentation/Hardware.md)

We may give our middle school students a microSD card with everything "ready to go". They won't need to figure out how to install all of the dependencies listed below! If you are a teacher and are having trouble following the instructions below, please reach out to me directly (Scott Feister), and I will be happy to share with you a microSD card image that has everything already installed.

See our [Hackaday project page](https://hackaday.io/project/28159) for a few additional details, though it may not be as up-to-date!

## Physical pre-requisites

You will need to build certain circuits before running the Python scripts; for example, you can't test a button if it's not wired to the Raspberry Pi! Circuit and connections diagrams for the five-string laser harp are available, as a PDF, in the "diagrams" directory. You can follow these diagrams to construct the physical circuits that go along with this Python code.

For more information on the physical construction of the five-string laser harp we are using for the middle school project, you should follow instructions on our [Hackaday project page](https://hackaday.io/project/28159). As of Spring 2018, we are in the process of writing our instructions, so stay 'tuned'!

## Installing dependencies on your Raspberry Pi

This toolkit has software dependencies:

* jackd (JACK Audio Connection Kit - http://www.jackaudio.org/)
* fluidsynth

It also has Python package dependencies:

* rpi.gpio
* gpiozero
* numpy
* pyfluidsynth

And the following additional dependencies:

* fluid-soundfont-gs (or any "Soundfont" for playback of MIDI)

The rpi.gpio and gpiozero Python libraries enables us to measure digital inputs on the Raspberry Pi: useful for noticing the fast change in signal from a phototransistor when the laser beam is blocked, and also useful for noticing when a button is pressed. The pyfluidsynth Python library lets us generate MIDI signals representing musical notes, and control fluidsynth. MIDI signals and synthesizer audio is processed by JACK and fluidsynth (a 'software synthesizer'). Together, these enable low-latency audio mixing of the sounds of "plucked" harp strings on our external speakers.

These dependencies, and a few others, can be installed onto your Raspberry Pi (tested on Raspbian Buster) as follows:

1. First, update your Raspbian Buster package repositories:
   
   ```bash
   sudo apt update
   ```

2. Next, install all the dependencies we discussed above via:
   
   ```bash
   sudo apt install jackd fluidsynth python3-pip python3-numpy python3-gpiozero python3-rpi.gpio fluid-soundfont-gs
   sudo pip3 install pyfluidsynth
   ```

You may also install optional additional software for additional control and troubleshooting of your software synthesizer setup:

```bash
sudo apt install qsynth patchage qjackctl vmpk
```

The optional software is as follows: Qsynth is a graphical interface for fluidsynth. Qjackctl is a graphical interface for JACK.  Patchage is a graphical interface for making software connections between various audio and MIDI components running in JACK. Vmpk is a software musical keyboard.

### Installing twang on your Raspberry Pi

After installing all of the required dependencies (see previous section), you are ready to install **twang**.

One way to install **twang** is via

```bash
sudo pip3 install git+https://github.com/phyzicist/twang.git
```

To update **twang** at a later date

```bash
sudo pip3 install --upgrade git+https://github.com/phyzicist/twang.git
```

## Command-line tools

## Running the harp

After physical construction of the laser harp:

1. Check you have audio output working with your speakers. Test this by trying to play a sound file in a standard Raspbian sound player, like Audacity. If you don't hear sound, you can change between HDMI audio, analog audio, and other audio output options by left-clicking the volume icon found in the upper right corner of the Raspbian desktop.

2. Create an instrument file. For example, you may choose to download and copy "harp.py" from the examples/ folder of this repository into "/home/pi/guitar.py" of your Raspberry Pi.

3. Set the environment variable "INSTRUMENT" to specify the python script you'd like to use, e.g., harp.py from this repository's examples folder. You can do this by the following command:
   ```export INSTRUMENT=/home/pi/guitar.py```

4. Finally, start your instrument (the JACK audio server, fluidsynth, and your instrument script), all by a single call to the included 'startsynth' script (located in the bin/ folder of this repository; it should be automagically installed into your path when you install the twang python package.)
   ```startsynth```

## Uninstalling

To uninstall **twang**

```bash
pip3 uninstall twang
```

## Credits

This project was created by Alex Wulff (DeAnza Academy of Technology and the Arts), Scott Feister (California State University Channel Islands), and Phil Hampton (California State University Channel Islands). We originally designed, built, and interactively displayed the five-string laser harp for K-8 children at the [CSUCI Annual Science Carnival](https://www.csuci.edu/sciencecarnival/) in November 2017. It was a big hit, so we have decided to develop it into a middle school project!

### Circuit diagrams

We made the laser harp circuit diagrams using the free, open-source vector graphics software [Inkscape](https://www.audacityteam.org/). Vector graphics (*.svg* format) for circuit elements, warning symbols, and more were gathered from [Wikimedia Commons](https://commons.wikimedia.org) and incorporated into the laser harp diagrams. I found this [collection of electrical symbols](https://commons.wikimedia.org/wiki/File:Electrical_symbols_library.svg) and this [laser warning symbol](https://commons.wikimedia.org/wiki/File:Laser-symbol.svg) particularly helpful.
