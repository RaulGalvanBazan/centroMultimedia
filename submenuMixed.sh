#! /bin/bash
if [ -d "$1"/"$2" ]; then
   ./submenuMixed.py "$1" "$2" "$3" "$4"
else
   pkill menu.py
   ./menu.py
fi
