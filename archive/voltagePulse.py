import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(1, GPIO.OUT)
while True:
    GPIO.output(1, True)
    time.sleep(10)
    GPIO.output(1, False)
    time.sleep(10)
