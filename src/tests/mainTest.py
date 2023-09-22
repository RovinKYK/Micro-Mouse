# Use fake_rpi for testing on PC
# Uncomment this when running on RPi
import RPi.GPIO as IO
#from fake_rpi.RPi import GPIO as IO
import time


# variables
leftMotorEnPin = 12
'''rightMotorEnPin = 10
'''

leftMotorDirPin1 = 15
leftMotorDirPin2 = 19
rightMotorDirPin1 = 21
rightMotorDirPin2 = 23

motorsPWMFrequency = 100
motorSpeed = 100

# setting the mode how to read the pins
IO.setmode(IO.BOARD)

# setting pin I/O
IO.setup(leftMotorEnPin, IO.OUT)
IO.setup(leftMotorDirPin1, IO.OUT)
IO.setup(leftMotorDirPin2, IO.OUT)
#IO.setup(rightMotorEnPin, IO.OUT)

# setting motor directions
IO.output(leftMotorDirPin1, IO.HIGH)
IO.output(leftMotorDirPin2, IO.LOW)

# setting pwm frequency for each pin
motorPWM1 = IO.PWM(leftMotorEnPin, motorsPWMFrequency)
#motorPWM2 = IO.PWM(rightMotorEnPin, motorsPWMFrequency)

motorPWM1.start(motorSpeed)
time.sleep(5)
motorPWM1.stop()
time.sleep(5)
'''motorPWM2.start(motorSpeed)
time.sleep(5)
motorPWM2.stop()
time.sleep(5)
'''
IO.cleanup()
