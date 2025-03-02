
## Installing dependencies on your Raspberry Pi

This toolkit has software dependencies:

* jackd ([JACK Audio Connection Kit](http://www.jackaudio.org/))
* fluidsynth

It also has Python package dependencies:

* rpi.gpio
* gpiozero
* numpy
* jack ([JACK Client for Python](https://jackclient-python.readthedocs.io/en/0.5.1/))
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
   sudo apt install jackd fluidsynth python3-pip python3-numpy python3-gpiozero python3-rpi.gpio python3-jack-client fluid-soundfont-gs
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
sudo pip3 install git+https://github.com/sfeister/twang.git
```

To update **twang** at a later date

```bash
sudo pip3 install --upgrade git+https://github.com/sfeister/twang.git
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
