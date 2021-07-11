import unicornhat as uh
from tallypi.webapp.light.base import AbstractLight
import logging
import inspect

logger = logging.getLogger('light')

class Light(AbstractLight):
    name = 'light'
    keyword = 'light'

    def __init__(self):
        uh.set_layout(uh.PHAT)

    def __del__(self):
        uh.off()

    def setColor(self, red, green, blue):
        uh.set_all(int(red), int(green), int(blue))
        uh.show()

    def getColor(self):
        return uh.get_pixel(0, 0)

    def setBrightness(self, percent):
        brightness = self.validateBrightness(percent)
        uh.brightness(brightness)

    def getBrightness(self):
        return uh.get_brightness()

    def shutdown(self):
        uh.off()

    # This is invoked when installed as a Bottle plugin
    def setup(self, app):
        logger.info("Loading Unicorn pHat")

        self.routes = app

        for other in app.plugins:
            if not isinstance(other, Light):
                continue
            if other.keyword == self.keyword:
                raise PluginError("Found another instance of the Unicorn pHat driver running!")

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
