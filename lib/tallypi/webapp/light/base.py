import time
import logging

logger = logging.getLogger('light')

class AbstractLight:
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
