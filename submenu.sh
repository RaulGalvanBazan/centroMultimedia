#! /bin/bash
if [[ -d "$1" ]]; then
   pkill menu.py
   ./menu.py "$1" "$2" "$3" "$4"
else
   pkill menu.py
   ./menu.py
fi
