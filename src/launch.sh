#!/bin/bash

clear

# Start the mpv player BEFORE mididings, so that mididings can connect to it and send commands to it.
bash ./start_mpv.sh

# Start mididings
deactivate > /dev/null 2>&1
source ~/.venv/mididings/bin/activate

python3 app.py main.py >| script.py
mididings -f script.py
