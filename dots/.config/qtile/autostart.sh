#!/bin/sh
xrandr --output Virtual1 --mode 1920x1080 &
nitrogen --restore &
picom &
rofi -show drun 6669 &

