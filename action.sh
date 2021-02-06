#! /bin/bash
if [[ "$1" == "kill" ]]; then
   echo "Reiniciando menu"
   pkill menu.py
   ./menu.py
elif [[ -d "$1" ]]; then
   pkill vlc
   pkill firefox
   cd "$1"
   if [[ "$2" == "audio" ]]; then
      vlc -f -L --audio-visual=visual --effect-list=spectrometer $3
   elif [[ "$2" == "video" ]]; then
      vlc -f -L "$3"
   elif [[ "$2" == "image" ]]; then
      vlc -f -L $3
   else
      echo "Opcion desconocida"
   fi
else
   echo "Medio no encontrado"
   pkill menu.py
   echo "Reiniciando menu"
   ./menu.py
fi

