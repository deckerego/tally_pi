import RPi.GPIO as GPIO
import subprocess

class PowerSwitch():
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(3, GPIO.FALLING, callback=self._callback)

    def _callback(self, channel):
        self.shutdown()

    def shutdown(self):
        subprocess.call(['shutdown', '-h', 'now'], shell=False)
