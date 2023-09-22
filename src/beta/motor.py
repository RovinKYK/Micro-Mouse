# This module cis the low level controller for the motors
import RPi.GPIO as IO


class Motor:
    FORWARD = (IO.LOW, IO.HIGH)
    BACKWARD = (IO.HIGH, IO.LOW)
    LOCK = (IO.HIGH, IO.HIGH)

    def __init__(self, EN_PIN, DIR_1_PIN, DIR_2_PIN):
        IO.setwarnings(False)

        self.EN_PIN = EN_PIN
        self.DIR_1_PIN = DIR_1_PIN
        self.DIR_2_PIN = DIR_2_PIN
        self.PWM_FREQ = 256

        # Initialize IO pins
        IO.setmode(IO.BOARD)
        IO.setup(EN_PIN, IO.OUT)
        IO.setup(DIR_1_PIN, IO.OUT)
        IO.setup(DIR_2_PIN, IO.OUT)

        self.motorPWM = IO.PWM(EN_PIN, self.PWM_FREQ)
        self.motorSpeed = 0.0
        self.motorPWM.start(self.motorSpeed)

    def setMotorSpeed(self, speed):
        self.motorSpeed = speed

    def setDirection(self, direction):
        IO.output(self.DIR_1_PIN, direction[0])
        IO.output(self.DIR_2_PIN, direction[1])

    def move(self):
        self.motorPWM.ChangeDutyCycle(self.motorSpeed)

    def stopMoving(self):
        self.setMotorSpeed(0)
        self.motorPWM.ChangeDutyCycle(0)

    def shutdown(self):
        self.motorPWM.stop()
