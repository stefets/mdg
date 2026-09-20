#!/usr/bin/env python
#-*- coding: utf-8 -*-

% for item in items:
    % with open(item, 'r') as file:
        ${file.read()}
    % endwith
% endfor
