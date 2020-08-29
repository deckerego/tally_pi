import unicornhat as uh
import time

uh.set_layout(uh.PHAT)

def setBrightness(percent):
    uh.brightness(percent)

def validateColor(intensity):
    if intensity < 0:
        return 0
    elif intensity > 255:
        return 255
    else:
        return intensity


def setColor(red, green, blue):
    for x in range(8):
        for y in range(4):
            uh.set_pixel(x, y, validateColor(red), validateColor(green), validateColor(blue))
    uh.show()

def getColor():
    return uh.get_pixel(0, 0)

def goToColor(r, g, b, steps=8, wait=0.05):
    rSrc, gSrc, bSrc = getColor()
    rStep = (r - rSrc) / steps
    gStep = (g - gSrc) / steps
    bStep = (b - bSrc) / steps

    while steps > 0:
        rSrc, gSrc, bSrc = getColor()
        setColor(rSrc + rStep, gSrc + gStep, bSrc + bStep)
        steps -= 1
        time.sleep(wait)

setBrightness(0.5)
setColor(0, 0, 255)
time.sleep(2.0)
goToColor(0, 255, 0)
time.sleep(2.0)
goToColor(255, 0, 0)
time.sleep(2.0)
goToColor(0, 0, 255)
time.sleep(2.0)
