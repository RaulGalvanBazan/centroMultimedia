#! /bin/bash
pkill vlc
pkill firefox
if [ -d "$1" ]; then
   cd "$1"
   vlc -f -L --audio-visual=visual --effect-list=spectrometer $2
else
   pkill menu.py
   ./menu.py
fi
