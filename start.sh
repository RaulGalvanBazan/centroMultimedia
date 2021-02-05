#! /bin/bash
pkill firefox
pkill vlc
firefox --kiosk $1
