#!/bin/bash
cd /home/pi/Desktop/sprayerv2
export FLASK_APP=facespray.py
sleep 1
python3 -m flask run