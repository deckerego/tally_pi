#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import json

logging.basicConfig(level=logging.WARN, format='%(levelname)-8s %(message)s')
logger = logging.getLogger('tallypi')

console = logging.StreamHandler()
console.setLevel(logging.WARNING)
logger.addHandler(console)

from tallypi.config import configuration
from bottle import Bottle, get, request
from light import Light
from powerswitch import PowerSwitch

application = Bottle()
light = Light()
power_switch = PowerSwitch()

def _to_json(r, g, b, bright):
    return '{ "red": %i, "green": %i, "blue": %i, "brightness": %f }' % (r, g, b, bright)

@application.get('/status')
def light_status():
    red, green, blue = light.getColor()
    brightness = light.getBrightness()
    return _to_json(red, green, blue, brightness)

@application.get('/set')
def light_set():
    color_hex = request.query.color
    bright_pct = request.query.brightness

    red = int(color_hex[0:2], 16)
    green = int(color_hex[2:4], 16)
    blue = int(color_hex[4:6], 16)
    brightness = float(bright_pct or 0.5)

    light.setBrightness(brightness)
    light.goToColor(red, green, blue)

    return _to_json(red, green, blue, brightness)
