#! /bin/bash
pkill vlc
if [ -d "$1" ]; then
   cd "$1"
   vlc -f -L --audio-visual=visual --effect-list=spectrometer ./
else
   pkill menu.py
   /home/pi/menu.py
fi
