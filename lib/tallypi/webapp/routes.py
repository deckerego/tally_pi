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

application = Bottle()
light = Light()

@application.get('/status')
def light_status():
    red, green, blue = light.getColor()
    return '{ "red": %i, "green": %i, "blue": %i }' % (red, green, blue)

@application.get('/set')
def light_set():
    colorHex = request.query.color
    redInt = int(colorHex[0:2], 16)
    greenInt = int(colorHex[2:4], 16)
    blueInt = int(colorHex[4:6], 16)

    light.setBrightness(0.5)
    light.goToColor(redInt, greenInt, blueInt)

    return '{ "red": %i, "green": %i, "blue": %i }' % (redInt, greenInt, blueInt)
