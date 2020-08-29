#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import logging
import json

logging.basicConfig(level=logging.WARN, format='%(levelname)-8s %(message)s')
logger = logging.getLogger('tallypi')

console = logging.StreamHandler()
console.setLevel(logging.WARNING)
logger.addHandler(console)

from tallypi.config import configuration
from bottle import Bottle, get

application = Bottle()

@application.get('/status')
def light_status():
    return '{ "status": "%s" }' % 'TBD'
