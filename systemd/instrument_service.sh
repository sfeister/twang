# Systemd service to run the instrument in the background
# Created by Scott Feister June 8, 2024
#   with some help from https://www.linode.com/docs/guides/start-service-at-boot/

DATE=`date '+%Y-%m-%d %H:%M:%S'`
echo "Instrument service started at ${DATE}" | systemd-cat -p info


until [ -e /dev/snd/pcmC0D0p ]
do
     sleep 5 && echo "Waiting on /dev/snd/pcmC0D0p to appear - the stereo bonnet"
done
echo "PCM stereo bonnet sound card found, proceeding"


if [ -z "$INSTRUMENT" ]
then
    echo "\$INSTRUMENT variable empty. Setting to default value: /home/musician/myinstrument.py"
    export INSTRUMENT="/home/musician/myinstrument.py"
fi

echo "\$INSTRUMENT environment variable: $INSTRUMENT"

echo "Killing off any existing processes locking hw:0 audio card"
fuser -v /dev/snd/pcmC0D0p
fuser -k /dev/snd/pcmC0D0p

echo "Enabling headless operation of Jack"
export JACK_NO_AUDIO_RESERVATION=1

echo "Loading in our custom python environment"
source /home/musician/jack-venv/bin/activate

echo "Starting instrument"
python $INSTRUMENT
