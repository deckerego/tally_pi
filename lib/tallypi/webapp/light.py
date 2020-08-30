import unicornhat as uh
import time

class Light():
    def __init__(self):
        uh.set_layout(uh.PHAT)

    def setBrightness(self, percent):
        uh.brightness(percent)

    def validateColor(self, intensity):
        if intensity < 0:
            return 0
        elif intensity > 255:
            return 255
        else:
            return intensity

    def setColor(self, red, green, blue):
        for x in range(8):
            for y in range(4):
                uh.set_pixel(x, y, self.validateColor(red), self.validateColor(green), self.validateColor(blue))
        uh.show()

    def getColor(self):
        return uh.get_pixel(0, 0)

    def goToColor(self, r, g, b, steps=8, wait=0.05):
        rSrc, gSrc, bSrc = self.getColor()
        rStep = (r - rSrc) / steps
        gStep = (g - gSrc) / steps
        bStep = (b - bSrc) / steps

        while steps > 0:
            rSrc, gSrc, bSrc = self.getColor()
            self.setColor(rSrc + rStep, gSrc + gStep, bSrc + bStep)
            steps -= 1
            time.sleep(wait)

        self.setColor(r, g, b)
