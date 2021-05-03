import RPi.GPIO as GPIO
from time import sleep


def motorInit():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    m1A = 36
    m1B = 38
    m1E = 40
    GPIO.setup(m1A, GPIO.OUT)
    GPIO.setup(m1B, GPIO.OUT)
    GPIO.setup(m1E, GPIO.OUT)
    return


def motorControl(setting):
    motorInit()
    GPIO.setmode(GPIO.BOARD)
    Motor1A = 36
    Motor1B = 38
    Motor1E = 40
    if setting == 'Coarse':
        GPIO.output(Motor1A, GPIO.HIGH)
        GPIO.output(Motor1B, GPIO.LOW)
    if setting == 'Fine':
        GPIO.output(Motor1A, GPIO.LOW)
        GPIO.output(Motor1B, GPIO.HIGH)
    GPIO.output(Motor1E, GPIO.HIGH)
    return


def motorKill():
    motorInit()
    GPIO.setmode(GPIO.BOARD)
    Motor1E = 40
    GPIO.output(Motor1E, GPIO.LOW)
    return
