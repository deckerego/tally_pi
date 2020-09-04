import unicornhat as uh
import time
import logging
import inspect

logger = logging.getLogger('light')

class Light():
    name = 'light'
    keyword = 'light'

    def __init__(self):
        uh.set_layout(uh.PHAT)

    def __del__(self):
        uh.off()

    def validateColor(self, intensity):
        if intensity < 0:
            return 0
        elif intensity > 255:
            return 255
        else:
            return intensity

    def validateBrightness(self, intensity):
        if intensity < 0.0:
            return 0.0
        if intensity > 0.0 and intensity < 0.2:
            return 0.2
        elif intensity > 1.0:
            return 1.0
        else:
            return intensity

    def setColor(self, red, green, blue):
        uh.set_all(red, green, blue)
        uh.show()

    def getColor(self):
        return uh.get_pixel(0, 0)

    def setBrightness(self, percent):
        brightness = self.validateBrightness(percent)
        uh.brightness(brightness)

    def getBrightness(self):
        return uh.get_brightness()

    def goToColor(self, r, g, b, steps=4, wait=0.05):
        if not steps:
            steps = 1

        red = self.validateColor(r)
        green = self.validateColor(g)
        blue = self.validateColor(b)

        rSrc, gSrc, bSrc = self.getColor()
        rStep = (red - rSrc) / steps
        gStep = (green - gSrc) / steps
        bStep = (blue - bSrc) / steps

        while steps > 1:
            rSrc, gSrc, bSrc = self.getColor()
            self.setColor(rSrc + rStep, gSrc + gStep, bSrc + bStep)
            steps -= 1
            time.sleep(wait)

        self.setColor(r, g, b)

    def test(self):
        self.setBrightness(0.5)
        self.goToColor(255, 0, 0, 10, 0.1)
        self.goToColor(0, 255, 0, 10, 0.1)
        self.goToColor(0, 0, 255, 10, 0.1)
        self.goToColor(255, 0, 0, 10, 0.1)
        self.goToColor(255, 255, 255, 1, 0.01)
        self.shutdown()

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
