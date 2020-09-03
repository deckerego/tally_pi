import RPi.GPIO as GPIO
import subprocess

def shutdown():
    subprocess.call(['shutdown', '-h', 'now'], shell=False)

class PowerSwitch():
    _callbacks = []
    _channel = 3

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        if GPIO.input(self._channel):
            GPIO.add_event_detect(self._channel, GPIO.FALLING, callback=self.__callback)
        else:
            GPIO.add_event_detect(self._channel, GPIO.RISING, callback=self.__callback)
        self.add_callback(shutdown)

    def __callback(self, channel):
        while self._callbacks:
            self._callbacks.pop()()

    def add_callback(self, function):
        self._callbacks.append(function)
