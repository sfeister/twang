## Raspberry Pi 4 FluidSynth MIDI Sound Engine
## 2019 - KOOP Instruments (koopinstruments@gmail.com)
## MODIFIED by Scott Feister in March 2025

echo "Starting synth script in 5 seconds (press Ctrl-c to cancel)..."
sleep 1
echo "4..."
sleep 1
echo "3..."
sleep 1
echo "2..."
sleep 1
echo "1..."
sleep 1

## Optional power saving (uncomment if desired):
# sudo ifconfig wlan0 down  # Disable the Wi-Fi adapter
# sudo tvservice --off  # Disable HDMI video output

echo "Killing any existing fluidsynth processes..."

sudo killall -s SIGKILL fluidsynth &>/dev/null


#### EDIT THIS LINE AS NEEDED
# Run 'cat /proc/asound/cards' to get a list of audio devices, and modify the grep statement below with a unique identifying string
audioDevice=$(cat /proc/asound/cards | grep "USB-Audio - AB13X USB Audio" | awk -F" " '{ print $1 }')  # Amazon off-brand sound card

echo "audioDevice: ${audioDevice}"

if pgrep -x "fluidsynth" > /dev/null
then
    echo "Fluidsynth is already running. It shouldn't be! I thought we just killed it."
    sleep 1
else
    echo "Starting fluidsynth server..."
    # Blink both lights to let the user know that the synth is starting
    sudo echo 1 | sudo tee /sys/class/leds/led0/brightness &>/dev/null
    sudo echo 1 | sudo tee /sys/class/leds/led1/brightness &>/dev/null
    sudo echo 0 | sudo tee /sys/class/leds/led0/brightness &>/dev/null
    sudo echo 0 | sudo tee /sys/class/leds/led1/brightness &>/dev/null
    sudo echo 1 | sudo tee /sys/class/leds/led0/brightness &>/dev/null
    sudo echo 1 | sudo tee /sys/class/leds/led1/brightness &>/dev/null
    sudo echo 0 | sudo tee /sys/class/leds/led0/brightness &>/dev/null
    sudo echo 0 | sudo tee /sys/class/leds/led1/brightness &>/dev/null
    sudo echo 1 | sudo tee /sys/class/leds/led0/brightness &>/dev/null
    sudo echo 1 | sudo tee /sys/class/leds/led1/brightness &>/dev/null
    sudo echo 0 | sudo tee /sys/class/leds/led0/brightness &>/dev/null
    sudo echo 0 | sudo tee /sys/class/leds/led1/brightness &>/dev/null
    # Start the FluidSynth server in a new screen session to allow reattaching for troubleshooting purposes
    
    #### EDIT THIS LINE AS NEEDED
    screen -dmS FluidSynth0 bash -c "sudo nice -n -20 fluidsynth -i -s -g 0.7 -a alsa -o audio.alsa.device=hw:$audioDevice --sample-rate=48000 --audio-bufcount=2 --audio-bufsize=64 -o synth.cpu-cores=4 -o synth.polyphony=128 /home/musician/mysounds.sf2"
    
    echo "FluidSynth started"
    sleep 2
fi

# Run the rest of the script on a loop in case a new sound card is connected, the FluidSynth server crashes, or a new MIDI instrument is connected
while [[ 1 -eq 1 ]]; do

    ## Enable one light to let the user know that device discovery is running
    echo 1 | sudo tee /sys/class/leds/led1/brightness &>/dev/null

    # Scrape the ALSA port number of the FluidSynth Server    
    fsClientNum=$(aconnect -o | grep "FLUID Synth" | awk -F" " '{ print $2 -0 }')
    
    echo "Device discovery active... (fsClientNum: ${fsClientNum})"

    # Connect every possible MIDI port to FluidSynth (This is what we mean by device "discovery".)

    myCounter=1
    while [[ $myCounter -lt $fsClientNum ]]; do
        aconnect $myCounter:0 $fsClientNum:0 2>/dev/null
        let myCounter=myCounter+1
    done

    echo 0 | sudo tee /sys/class/leds/led1/brightness &>/dev/null

    sleep 1

done
