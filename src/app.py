#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import sys
import json
import alsaaudio
from mako.template import Template


def render_asoundrc(config) -> None:
    audio_devices = config["asoundrc"]
    asoundrc = Template(filename=config["template"])
    for device_number, card_name in enumerate(alsaaudio.cards()):
        audio_devices[card_name] = f"hw:{device_number},0"
    with open(os.path.expanduser('~') + "/.asoundrc", "w") as FILE:
        FILE.write(asoundrc.render(**audio_devices))


def render_script(config) -> str:
    # Generates the mididings script code
    return Template(filename=config["template"]).render(
        includes = config["includes"]
    )

def render(config) -> str:
    render_asoundrc(config["alsa"])
    return render_script(config)

def main(args = None) -> int:
    with open('config.json') as FILE:
        config = json.load(FILE)
    print(render(config))


'''
    Entry point
'''

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]) or 0)
