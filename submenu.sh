#! /bin/bash
#Scrip para desplegar un menú con la lista de archivos a mostrar
#Primero se revisa que la ruta del usb dada como argumento exista, si no
#se reinicia el menú principal
#Autores:
#  Fernández Mora JosÉ Enrique
#  Galván Bazán Raúl
#  Sánchez Castillo Paola
#Licencia: MIT
if [[ -d "$1" ]]; then
   pkill menu.py
   ./menu.py "$1" "$2" "$3" "$4"
else
   pkill menu.py
   ./menu.py
fi
