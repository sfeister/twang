# twang

Raspberry Pi Pico CircuitPython library, with examples, for building a MIDI electronic instrument which uses a laser, LED, or other kind of light source as its "strings". Pretty much anything that relies on breaking a light beam to make some sounds!

This repository also holds scripts to make MIDI-synthesizer out of the Raspberry Pi 4.

You can make a Laser Harp, Optical Piano, Laser Ukelele, Laser Guitar, etc. using electronics and a Pi Pico, and then plug it into the synthesizer via a USB cable. 

Goals of this wider project are learning about circuits, CAD, and computer programming.

The "twang" library is meant to be run on a Pi Pico microcontroller, via CircuitPython.

The accompanying Linux scripts (for the synthesizer) are meant to be run on a Raspberry Pi 4 computer.

## Getting Started

If you are a middle schooler, middle school teacher, or someone just interested in building an instrument, you can skip the rest of this page and instead follow directions from the following three pages (in order):

1. [Safe Design and Usage of a Laser Instrument](documentation/Safety.md)

2. [Building the Instrument Hardware](documentation/Hardware.md)

3. [Flashing your Pico with CircuitPython](documentation/Pico.md)

4. [(Advanced) Preparing a Raspberry Pi 4 to be an MIDI synthesizer](documentation/Synthesizer.md)

For Step 4, we may give our middle school students a microSD card with everything "ready to go". They won't need to figure out how to install all of the dependencies listed below! If you are a teacher and are having trouble following the instructions below, please reach out to me directly (Scott Feister), and I will be happy to share with you a microSD card image that has everything already installed.

## Physical pre-requisites

You will need to build certain circuits before programming your Pi Pico; for example, you can't test a button if it's not wired to the Pi Pico! Circuit and connections diagrams for a ten-string laser harp and a six-string laser guitar are available, as a PDF, in the "diagrams" directory. You can follow these diagrams to construct the physical circuits that go along with this Python code.

## Credits

This project was created by Alex Wulff (DeAnza Academy of Technology and the Arts), Scott Feister (California State University Channel Islands), and Phil Hampton (California State University Channel Islands). We originally designed, built, and interactively displayed the five-string laser harp for K-8 children at the [CSUCI Annual Science Carnival](https://www.csuci.edu/sciencecarnival/) in November 2017. It was a big hit, so we have decided to develop it into a middle school project!

### Circuit diagrams

We made the laser harp circuit diagrams using the free, open-source vector graphics software [Inkscape](https://www.audacityteam.org/). Vector graphics (*.svg* format) for circuit elements, warning symbols, and more were gathered from [Wikimedia Commons](https://commons.wikimedia.org) and incorporated into the laser harp diagrams. I found this [collection of electrical symbols](https://commons.wikimedia.org/wiki/File:Electrical_symbols_library.svg) and this [laser warning symbol](https://commons.wikimedia.org/wiki/File:Laser-symbol.svg) particularly helpful.