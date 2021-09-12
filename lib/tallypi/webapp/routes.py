import logging
import socket

logging.basicConfig(level=logging.WARN, format='%(levelname)-8s %(message)s')
logger = logging.getLogger('tallypi')

console = logging.StreamHandler()
console.setLevel(logging.WARNING)
logger.addHandler(console)

from tallypi.config import configuration
from bottle import Bottle, route, request, response

light_module = configuration.get('light_module')
gpio_module = configuration.get('gpio_module')

if light_module == 'mock': from tallypi.webapp.light.mock import Light
elif light_module == 'blinkt': from tallypi.webapp.light.blinkt import Light
elif light_module == 'unicornhat': from tallypi.webapp.light.unicornhat import Light
else: from tallypi.webapp.light.neopixel import Light

if gpio_module == 'mock': from tallypi.webapp.powerswitch.mock import PowerSwitch
else: from tallypi.webapp.powerswitch.rpi import PowerSwitch

pHat = Light()
power_switch = PowerSwitch()
power_switch.add_callback(pHat.shutdown)

application = Bottle()
application.install(pHat)

def _to_json(r, g, b, bright):
    hostname = socket.gethostname()
    return '{ "hostname": "%s", "red": %i, "green": %i, "blue": %i, "brightness": %f }' % (hostname, r, g, b, bright)

@application.hook('after_request')
def connection():
    response.headers['Connection'] = 'Close'

@application.hook('after_request')
def access_control():
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

@application.route('/status')
def light_status(light):
    red, green, blue = light.getColor()
    brightness = light.getBrightness()

    response.content_type = 'application/json'
    return _to_json(red, green, blue, brightness)

@application.route('/set')
def light_set(light):
    color_hex = request.query.color
    bright_pct = request.query.brightness

    red = int(color_hex[0:2], 16)
    green = int(color_hex[2:4], 16)
    blue = int(color_hex[4:6], 16)
    brightness = float(bright_pct or 0.5)

    light.setBrightness(brightness)
    light.goToColor(red, green, blue)

    response.content_type = 'application/json'
    return _to_json(red, green, blue, brightness)
