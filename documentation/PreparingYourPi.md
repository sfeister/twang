# Preparing your Raspberry Pi to be an Instrument

By Dr. Scott Feister

January 15, 2020

In this guide, I will walk you through the first setup of your Raspberry Pi, the Pi Stereo Bonnet, and the *twang* software environment. The target audience is a middle school student or teacher. I assume no experience with Raspberry Pi and Linux, though it might be helpful to have access to someone with experience at points in this guide!

## Set up your SD card

##### Parts needed:

* Computer with internet (e.g. your laptop)
* 8 GB+ microSD card
* microSD card reader for your computer

##### At the end of this section you should:

- Have a microSD card with Raspbian installed on it

##### Instructions

Download the Raspbian operating system image onto your computer. I downloaded Raspbian from [this page](https://www.raspberrypi.org/downloads/raspbian/) at RaspberryPi.org, by following the "Download Zip" link beneath the header "Raspbian Buster with desktop". For the inquisitive among you, here are two additional notes:

* I downloaded the "with Desktop" version because it's a smaller download size, so downloads faster -- and I can always install more software later. You may also use the "with Desktop and software" version. The "Lite" version of Raspbian does not have any graphical desktop environment, and so the "Lite" version of Raspbian would be inappropriate for this project.
* The latest version of Raspbian may not be called "Buster" -- that's OK, it should still work. If you neverless want to match versions with me exactly, here is a [direct link](http://downloads.raspberrypi.org/raspbian/images/raspbian-2019-09-30/2019-09-26-raspbian-buster.zip).

Once your download has completed, plug your microSD card adapter into your computer, and install your downloaded image onto your microSD card. Don't just copy and paste! That doesn't work :-). I followed [these instructions](https://www.raspberrypi.org/documentation/installation/installing-images/README.md) from RaspberryPi.org and installed Raspbian into my microSD card using software called balenaEtcher.

## Make connections and boot up your Raspberry Pi

##### Parts needed:

* Raspberry Pi 3 or Raspberry Pi Zero W
  
  * HDMI adapter for Pi Zero W
  
  * USB adapters for Pi Zero W

* Power supply for Pi

* USB keyboard & mouse

* A monitor with an HDMI cable

* Your microSD card

##### At the end of this section you should:

* Be able to boot into the desktop on your Raspberry Pi

##### Instructions

Make all the connections, boot up, and familiarize yourself with the Raspberry Pi. With one caveat, you should follow [these instructions](https://projects.raspberrypi.org/en/projects/raspberry-pi-getting-started) from RaspberryPi.org. The caveat is, when you get to the page titled "Set up your SD card", you can skip that page because you've already set up your SD card!

## Get oriented in Raspbian

##### Parts needed:

* Your Raspberry Pi, booted up to the home screen

##### At the end of this section you should:

* Know the basics of using your Raspberry Pi
* Be able to use a web browser from your Raspberry Pi to surf the internet

##### Instructions

Follow all [these instructions](https://projects.raspberrypi.org/en/projects/raspberry-pi-using) from RaspberryPi.org to get oriented with your new Raspberry Pi system. Here are a few additional notes:

* Pay special attention to the "Connecting to the internet", "Accessing your files", and "Using the terminal" pages.

* When you get to the "Setting up sound" step, note that the Raspberry Pi Zero W does not have an "analog" audio output jack (but can still send sound through HDMI.) In our case, we will use neither "analog" nor "HDMI"; we will be using the [Pi Stereo Speaker Bonnet](https://www.adafruit.com/product/3346) for our audio, which is a third (unlisted) option.

Craving more exploration before moving on? Check out [this exploratory pathway](https://projects.raspberrypi.org/en/pathways/getting-started-with-raspberry-pi) on RaspberryPi.org.

## Physically construct and install software for the Pi Stereo Speaker Bonnet

##### Parts needed:

- Your Raspberry Pi, booted up with an internet connection
- [Pi Stereo Speaker Bonnet](https://www.adafruit.com/product/3346) (not yet assembled)
- 2x [3W speakers]([https://www.adafruit.com/product/1314](https://www.adafruit.com/product/1314)
  - Alternatively, you can buy two [enclosed, pre-assembled, pre-wired speakers]([https://www.adafruit.com/product/1669](https://www.adafruit.com/product/1669).
- Connecting wires for speakers (two wires for each speaker, cut to length and stripped at the ends)
- Soldering station

#### Additionally, if you are new to soldering and/or Linux, you may wish to have access to these outside resources:

* An instructor to assist at the appropriate steps with learning how to solder

* An instructor to assist at the appropriate steps with troubleshooting your entry of terminal commands

##### At the end of this section you should have:

* Gained repeated experience with soldering pins
* Gained limited experience with the Linux terminal
* Be able to play sound out of your external 3W speakers

##### Instructions

We will use the [Pi Stereo Speaker Bonnet](https://www.adafruit.com/product/3346) to amplify and play audio out of external speakers. Getting this part set up involves some work with both soldering and software!

Follow all of [these instructions](https://learn.adafruit.com/adafruit-speaker-bonnet-for-raspberry-pi) to get up and running with your Pi Stereo Speaker Bonnet. This will take a little while! Make sure to do the speaker tests at the end of the tutorial, to verify that everything is working right.

## Install twang software and add-ons

##### Parts needed:

- Your Raspberry Pi, booted up with an internet connection

##### Additionally, if you are new to Linux, you may wish to have access to these outside resources::

- An instructor to assist throughout with troubleshooting and verifying the accurate entry of terminal commands

##### At the end of this section you should have:

- Lots of experience typing commands into the terminal

- The ability to run "stopsynth" and "startsynth" from the terminal, making your speakers pop and hiss

- An instrument that boots on startup

- Working power button software for whenever you are ready to install the power button hardware

##### Instructions

The following is an abridged/modified version of the instructions for installing twang that found in the README of [https://github.com/phyzicist/twang](https://github.com/phyzicist/twang).

###### Update system and install software dependencies

Open the terminal and `update `your software fully.

```bash
sudo apt -y update
sudo apt -y upgrade
```

Install all of the required and optional software dependencies for twang.

```bash
sudo apt -y install jackd fluidsynth python3-pip python3-numpy python3-gpiozero python3-rpi.gpio fluid-soundfont-gs qsynth patchage qjackctl vmpk
sudo pip3 install pyfluidsynth
```

###### Download a high-quality-guitar soundfont

"Soundfonts" are collections of musical instrument sounds. We will download a high-quality soundfont filled with a variety of guitar sounds. On the same website, there are also high-quality soundfonts for orchestras, piano, harp, and more!

Using your Raspberry Pi's web browser, go to the [Soundfonts4U website](https://sites.google.com/site/soundfonts4u/). Scroll down to the "Guitars-Universal-V1.5.sf2" link, follow it, and download it. Then, move that file into the folder "/usr/share/sounds/sf2/". For example, if you downloaded the file into the "Downloads" folder, you can move it with the command:

```bash
sudo mv ~/Downloads/Guitars-Universal-V1.5.sf2 /usr/share/sounds/sf2/
```

###### Install twang and example instruments

Install twang.

```bash
sudo pip3 install git+https://github.com/phyzicist/twang.git
```

Download and extract the example instruments from the twang GitHub repository. E.g. here is one way to download all example instruments into a folder called "twang_examples" in your home folder:

```bash
cd ~
git clone https://github.com/phyzicist/twang.git
mv twang/examples twang_examples
rm -rf twang
```

Verify that you now have a file called "guitar.py" in the folder "twang_examples" of your home folder.

###### Edit .bash_profile for automatic instrument startup

Next, you'll create and/or edit your ".bash_profile" file in your home folder. This file will be run every time you boot the pi (and more!), to locate the default guitar instrument and run the 'startsynth' command every time you boot up your Raspberry Pi.

1. Type the following command to create the file using the text editor "nano".

```bash
sudo nano ~/.bash_profile
```

2. Copy and paste the following text, exactly as written below, into the nano text editor. If text is already present in your nano text editor, you can paste this text afterwards.

```bash
#
# ~/.bash_profile
#

## DEFINE 'INSTRUMENT' ENVIRONMENT VARIABLE
# We use our own made-up "INSTRUMENT" environment variable to hold a path to our instrument's python3 script
# This script will run on startup, and is linked with the "startsynth" and "stopsynth" commands.
# Modify the path below and then reboot to change your instrument script to another file.

export INSTRUMENT="/home/pi/twang_examples/guitar.py"

## START YOUR INSTRUMENT
# Jack, our audio software, seems to have lots of drama when running headless on a Pi
# As a consequence, it can't be easily started by sudo
# The solution here is to put the start of jack and the synthesizer into .bash_profile
# (Solution copied from https://bbs.archlinux.org/viewtopic.php?id=146788)

# run startsynth iff jack is not already running:
ps -e | grep jack > /dev/null 2>&1 || (startsynth > /dev/null 2>&1 ; echo "Starting synthesizer")
```

3. Press ```Ctrl + X``` and then ```Y``` when prompted, to save the file and close the editor.

###### Add software for a power button

These next few steps are required to enable our manually-added hardware power button. Installing and using this power button is important to prevent the Pi SD card from being corrupted after abruptly unplugging the power -- however, the button does require some software setup, which I outline below.

The instructions below are copied from [this page](https://howchoo.com/g/mwnlytk3zmm/how-to-add-a-power-button-to-your-raspberry-pi) on Howchoo.com. More explanations and details are found on that page, but still follow the directions below (as they are somewhat modified for our particular usage)! The two scripts that are discussed in the webpage and that you download below work together to watch for a power button press, and may also do other actions beyond just sending the "shutdown" command when the power button is pressed (such as blinking the lasers -- look inside the scripts for more details).

1. Download the "listen-for-shutdown.sh" script from the twang repository into the system directory "/etc/init.d/". Note that the following is a SINGLE, long line of text, and it should be copied and pasted into the terminal all in one piece:

```bash
sudo wget https://raw.githubusercontent.com/phyzicist/twang/master/bin/listen-for-shutdown.sh -P /etc/init.d/
```

2. Download the "listen-for-shutdown.py" script from the twang repository into the system directory "/usr/local/bin/". Again, note that the following is a SINGLE, long line of text, and it should be copied and pasted into the terminal all in one piece:

```bash
sudo wget https://raw.githubusercontent.com/phyzicist/twang/master/bin/listen-for-shutdown.py -P /usr/local/bin/
```

3. Change permissions to make these two scripts executable.

```bash
sudo chmod +x /etc/init.d/listen-for-shutdown.sh
sudo chmod +x /usr/local/bin/listen-for-shutdown.py 
```

4. Register the "listen-for-shutdown.sh" script to be activated on next boot, and start it now as well.

```bash
sudo update-rc.d listen-for-shutdown.sh defaults
sudo /etc/init.d/listen-for-shutdown.sh start
```
