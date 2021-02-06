#! /bin/bash
#Script que ejecuta una aplicación dependiendo de la opción elegida por 
#el usuario en el menu
#Autores:
#  Fernández Mora JosÉ Enrique
#  Galván Bazán Raúl
#  Sánchez Castillo Paola
#Licencia: MIT

#Se reinicia el menú
if [[ "$1" == "kill" ]]; then
   echo "Reiniciando menu"
   pkill menu.py
   ./menu.py
#Se revisa si el argumento dado como la ruta de la usb existe
#Si la ruta existe se ejecuta la aplicación con los argumentos dados
#Si la ruta no existe se reinicia el menú principal
elif [[ -d "$1" ]]; then
   #Se detine la ejecuación de la aplicación anterior si existe
   pkill vlc
   pkill firefox
   #Se cambia a la ruta
   cd "$1"
   #Se ejecuta la aplicación dependiendo de los argumentos recibidos
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

