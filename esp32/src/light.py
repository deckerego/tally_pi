import neopixel
import board
import time

pixel_pin = board.NEOPIXEL
pixel_num = 50
pixels = neopixel.NeoPixel(pixel_pin, pixel_num, brightness=0.1, auto_write=False)
pixels.fill((0, 0, 0))
pixels.show()

def setColor(red, green, blue):
    pixels.fill((int(red), int(green), int(blue)))
    pixels.show()

def getColor():
    return pixels[0]

def setBrightness(percent):
    brightness = validateBrightness(percent)
    pixels.brightness = brightness
    pixels.show()
    return getBrightness()

def getBrightness():
    return pixels.brightness

def shutdown():
    setColor(0, 0, 0)
    setBrightness(0.0)

def validateColor(intensity):
    if intensity < 0:
        return 0
    elif intensity > 255:
        return 255
    else:
        return intensity

def validateBrightness(intensity):
    if intensity < 0.0:
        return 0.0
    if intensity > 0.0 and intensity < 0.2:
        return 0.2
    elif intensity > 1.0:
        return 1.0
    else:
        return intensity

def goToColor(r, g, b, steps=4, wait=0.05):
    if not steps:
        steps = 1

    red = validateColor(r)
    green = validateColor(g)
    blue = validateColor(b)

    rSrc, gSrc, bSrc = getColor()
    rStep = (red - rSrc) / steps
    gStep = (green - gSrc) / steps
    bStep = (blue - bSrc) / steps

    while steps > 1:
        rSrc, gSrc, bSrc = getColor()
        setColor(rSrc + rStep, gSrc + gStep, bSrc + bStep)
        steps -= 1
        time.sleep(wait)

    setColor(r, g, b)

def test():
    setBrightness(0.5)
    goToColor(255, 0, 0, 10, 0.1)
    goToColor(0, 255, 0, 10, 0.1)
    goToColor(0, 0, 255, 10, 0.1)
    goToColor(255, 0, 0, 10, 0.1)
    goToColor(255, 255, 255, 1, 0.01)
    shutdown()
