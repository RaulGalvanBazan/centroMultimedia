#! /bin/bash
#! /bin/bash
#Script que el navegador Firefox con la ruta del servicio
#de streaming seleccionado.
#Autores:
#  Fernández Mora JosÉ Enrique
#  Galván Bazán Raúl
#  Sánchez Castillo Paola
#Licencia: MIT

pkill firefox
pkill vlc
firefox --kiosk $1
