#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import json
import alsaaudio
from mako.template import Template


def generate_asoundrc(config) -> None:
    template = Template(filename="asoundrc.mako")
    audio_devices = config["asoundrc"]
    for device_number, card_name in enumerate(alsaaudio.cards()):
        audio_devices[card_name] = f"hw:{device_number},0"
    with open(os.path.expanduser("~") + "/.asoundrc", "w") as FILE:
        FILE.write(template.render(**audio_devices))


def generate_script(config) -> str:
    # Generates the mididings script code
    template = Template(filename="main.mako")
    return template.render(items=config["items"])


def main(args=None) -> int:
    with open("config.json") as FILE:
        config = json.load(FILE)
    generate_asoundrc(config)
    print(generate_script(config))  # Print the generated script to stdout


"""
    Entry point
"""

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]) or 0)
