import RPi.GPIO as GPIO
from time import sleep

redpin = 32
greenpin = 33
bluepin = 35


class RgbUtil():
    def __init__(self):
        redpin = 32
        greenpin = 33
        bluepin = 35
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(redpin, GPIO.OUT)
        GPIO.setup(greenpin, GPIO.OUT)
        GPIO.setup(bluepin, GPIO.OUT)

        red = GPIO.PWM(redpin, 1000)
        red.start(0)
        green = GPIO.PWM(greenpin, 1000)
        green.start(0)
        blue = GPIO.PWM(bluepin, 1000)
        blue.start(0)

        self.lights = [red, green, blue]

    def set_brightness(self, color, value):
        self.lights[color].ChangeDutyCycle(value)

    def turn_off(self):
        for light in self.lights:
            light.ChangeDutyCycle(0)
