#! /bin/bash
pkill vlc
pkill firefox
vlc -f -L "$1"
