#! /bin/bash
pkill vlc
if [ -d "$1" ]; then
   cd "$1"
   vlc -f -L ./
else
   pkill menu.py
   ./menu.py
fi
