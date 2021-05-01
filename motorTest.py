import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)

Motor1A = 36
Motor1B = 38
Motor1E = 40

GPIO.setup(Motor1A, GPIO.OUT)  # 2
GPIO.setup(Motor1B, GPIO.OUT)
GPIO.setup(Motor1E, GPIO.OUT)

try:
    print("Turning motor on config 1")
    GPIO.output(Motor1A, GPIO.HIGH)  # 3
    GPIO.output(Motor1B, GPIO.LOW)
    GPIO.output(Motor1E, GPIO.HIGH)
    sleep(5)
    print("Turning motor on config 2")
    GPIO.output(Motor1A, GPIO.LOW)  # 3
    GPIO.output(Motor1B, GPIO.LOW)
    GPIO.output(Motor1E, GPIO.HIGH)
    print("Turning motor on config 3")
    GPIO.output(Motor1A, GPIO.HIGH)  # 3
    GPIO.output(Motor1B, GPIO.HIGH)
    GPIO.output(Motor1E, GPIO.HIGH)
    print("Stopping motor")
    GPIO.output(Motor1E, GPIO.LOW)  # 4
finally:
    GPIO.output(Motor1E, GPIO.LOW)  # 5
    GPIO.cleanup()  # 6
