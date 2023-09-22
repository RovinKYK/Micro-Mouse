
# Use fake_rpi for testing on PC
from fake_rpi.RPi import GPIO
# Uncomment this when running on RPi
# import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

GPIO.setup(12, GPIO.OUT)
pwm = GPIO.PWM(12, 100)


dc = 0
pwm.start(dc)

try:
    while True:
        for dc in range(0, 101, 5):
            pwm.ChangeDutyCycle(dc)

            time.sleep(0.05)
            print(dc)
        for dc in range(95, 0, -5):
            pwm.ChangeDutyCycle(dc)

            time.sleep(0.05)
            print(dc)
except KeyboardInterrupt:
    print("Ctl C pressed - ending program")
finally:
    pwm.stop()
    GPIO.cleanup()
