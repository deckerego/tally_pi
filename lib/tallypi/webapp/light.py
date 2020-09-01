import unicornhat as uh
import time

class Light():
    def __init__(self):
        uh.set_layout(uh.PHAT)

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

        self.setColor(red, green, blue)
