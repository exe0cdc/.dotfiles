#!/bin/bash
killall compton
xrandr --output VIRTUAL1 --off --output DP3 --mode 1920x1080 --scale 1.5x1.5 --pos 0x0 --rotate right --output eDP1 --off --output DP1 --mode 3840x2160 --pos 1620x360 --rotate normal --output HDMI2 --off --output HDMI1 --off --output DP2 --off
compton --config ~/.config/compt.conf -b


