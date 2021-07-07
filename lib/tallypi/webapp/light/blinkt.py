import blinkt
from tallypi.webapp.light.base import AbstractLight
import logging
import inspect

logger = logging.getLogger('light')

class Light(AbstractLight):
    name = 'light'
    keyword = 'light'

    def __init__(self):
        blinkt.set_clear_on_exit(True)
        blinkt.clear()
        blinkt.show()

    def setColor(self, red, green, blue):
        blinkt.set_all(red, green, blue)
        blinkt.show()

    def getColor(self):
        r, g, b, brightness = blinkt.get_pixel(0)
        return r, g, b

    def setBrightness(self, percent):
        brightness = self.validateBrightness(percent)
        blinkt.set_brightness(brightness)
        blinkt.show()

    def getBrightness(self):
        r, g, b, brightness = blinkt.get_pixel(0)
        return brightness

    def shutdown(self):
        blinkt.clear()
        blinkt.show()

    # This is invoked when installed as a Bottle plugin
    def setup(self, app):
        logger.info("Loading Blinkt! pHat")

        self.routes = app

        for other in app.plugins:
            if not isinstance(other, Light):
                continue
            if other.keyword == self.keyword:
                raise PluginError("Found another instance of the Blinkt! pHat driver running!")

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
