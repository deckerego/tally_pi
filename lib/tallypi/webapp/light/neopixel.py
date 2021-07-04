from tallypi.webapp.light.base import AbstractLight
from tallypi.config import configuration
import board
import neopixel
import logging
import inspect

logger = logging.getLogger('light')

class Light(AbstractLight):
    name = 'light'
    keyword = 'light'

    def __init__(self):
        led_count = int(configuration.get('light_led_count'))
        self.pixels = neopixel.NeoPixel(board.D18, led_count, auto_write=False)

    def __del__(self):
        self.pixels.fill((0, 0, 0))
        self.pixels.brightness = 0.0
        self.pixels.show()

    def setColor(self, red, green, blue):
        self.pixels.fill((int(red), int(green), int(blue)))
        self.pixels.show()

    def getColor(self):
        return self.pixels[0]

    def setBrightness(self, percent):
        brightness = self.validateBrightness(percent)
        self.pixels.brightness = brightness
        self.pixels.show()
        return self.getBrightness()

    def getBrightness(self):
        return self.pixels.brightness

    def shutdown(self):
        self.setColor(0, 0, 0)
        self.setBrightness(0.0)

    # This is invoked when installed as a Bottle plugin
    def setup(self, app):
        logger.info("Loading NeoPixels")

        self.routes = app

        for other in app.plugins:
            if not isinstance(other, Light):
                continue
            if other.keyword == self.keyword:
                raise PluginError("Found another instance of the NeoPixel driver running!")

        self.test()

    # This is invoked within Bottle as part of each route when installed
    def apply(self, callback, context):
        conf = context.get('light') or {}
        keyword = conf.get('keyword', self.keyword)

        args = inspect.getargspec(callback)[0]
        if keyword not in args:
            return callback

        def wrapper(*args, **kwargs):
            kwargs[self.keyword] = self
            rv = callback(*args, **kwargs)
            return rv
        return wrapper

    # De-installation from Bottle as a plugin
    def close(self):
        self.shutdown()

class PluginError(Exception):
    pass

Plugin = Light
