from tallypi.webapp.light.base import AbstractLight
import logging
import inspect

logger = logging.getLogger('light')

class Light(AbstractLight):
    name = 'light'
    keyword = 'light'
    brightness = 0
    red, green, blue = 0, 0, 0

    def setColor(self, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue

    def getColor(self):
        return self.red, self.green, self.blue

    def setBrightness(self, percent):
        brightness = self.validateBrightness(percent)
        self.brightness = brightness

    def getBrightness(self):
        return self.brightness

    def shutdown(self):
        pass

    # This is invoked when installed as a Bottle plugin
    def setup(self, app):
        logger.info("Loading Mock Lighting Source")

        self.routes = app

        for other in app.plugins:
            if not isinstance(other, Light):
                continue
            if other.keyword == self.keyword:
                raise PluginError("Found another Mock Lighting Source driver running!")

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
