#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import argh
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


def render_script(config, template=None) -> str:
    # Generates the mididings script code
    return Template(filename=config["template"]).render(
        includes = config["includes"]
    )

def render(config, template) -> str:
    render_asoundrc(config["alsa"])
    return render_script(config, template)

def main(stemplate=None):
    with open('config.json') as FILE:
        config = json.load(FILE)
    print(render(config, stemplate))


'''
    Entry point
'''

argh.dispatch_command(main)
