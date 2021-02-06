#! /bin/bash
#Scrip para desplegar un menú con opciones para una usb con archivos 
#de tipos mixtos.
#Primero se revisa que la ruta del usb dada como argumento exista, si no
#se reinicia el menú principal
#Autores:
#  Fernández Mora JosÉ Enrique
#  Galván Bazán Raúl
#  Sánchez Castillo Paola
#Licencia: MIT
if [ -d "$1" ]; then
   pkill menu.py
   ./menu.py "$1" "$2" "$3"
else
   pkill menu.py
   ./menu.py
fi
