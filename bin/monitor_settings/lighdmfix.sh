#!/bin/bash

DP_STATUS=$(xrandr --listmonitors | grep DP-0)
HDMI_STATUS=$(xrandr --listmonitors | grep HDMI-0)

if [ "$HDMI_STATUS" != "" ] & [ "$DP_STATUS" != "" ]
then
	xrandr --dpi 144 --fb 5460x2880 --output DP-0 --mode 3840x2160 --output HDMI-0 --mode 1920x1080 --scale 1.5x1.5 --pos 3840x0 --rotate right
else
	echo "conditions not met"
	echo $HDMI_STATUS
	echo $DP_STATUS
fi



