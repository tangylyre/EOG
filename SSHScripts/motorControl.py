import RPi.GPIO as GPIO
from time import sleep
# this is a set of functions for the VIBRATIONAL OUTPUT unit.

def motorInit():
    # initializes the established motor driver ports.
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
    # outputs different power depending on the input argument setting.
    motorInit()
    GPIO.setmode(GPIO.BOARD)
    Motor1A = 36
    Motor1B = 38
    Motor1E = 40
    if setting == 'Coarse':
        # this is around 5V 500mA from memory, may need to verify
        GPIO.output(Motor1A, GPIO.HIGH)
        GPIO.output(Motor1B, GPIO.LOW)
    if setting == 'Fine':
        # this is around 5V 400mA from memory, may need to verify
        GPIO.output(Motor1A, GPIO.LOW)
        GPIO.output(Motor1B, GPIO.HIGH)
    GPIO.output(Motor1E, GPIO.HIGH)
    return


def motorKill():
    # kills motor operations. you need to call this before you end a
    # script or it will continue vibrating after a script runs.
    motorInit()
    GPIO.setmode(GPIO.BOARD)
    Motor1E = 40
    GPIO.output(Motor1E, GPIO.LOW)
    return
