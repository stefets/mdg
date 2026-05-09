#!/usr/bin/env python
#-*- coding: utf-8 -*-

'''
Thanks to the programmer Dominic Sacré for that unbeatable MIDI engine - a true masterpiece

https://github.com/mididings/mididings (Community version! My prayers have been answered)
'''

% for item in items:
    % with open(item, 'r') as file:
        ${file.read()}
    % endwith
% endfor
