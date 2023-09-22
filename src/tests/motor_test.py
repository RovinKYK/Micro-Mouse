# Use fake_rpi for testing on PC
# Uncomment this when running on RPi
import RPi.GPIO as IO
#from fake_rpi.RPi import GPIO as IO
import time

# variables
leftMotorEnPin = 11
rightMotorEnPin = 13

leftMotorDirPin1 = 15
leftMotorDirPin2 = 19
rightMotorDirPin1 = 21
rightMotorDirPin2 = 23



motorsPWMFrequency = 128
motorSpeed = 0

#setting the mode how to read the pins
IO.setmode(IO.BOARD)


#setting pin I/O
IO.setup(leftMotorEnPin, IO.OUT)
IO.setup(rightMotorEnPin, IO.OUT)

IO.setup(leftMotorDirPin1, IO.OUT)
IO.setup(leftMotorDirPin2, IO.OUT)
IO.setup(rightMotorDirPin1, IO.OUT)
IO.setup(rightMotorDirPin2, IO.OUT)


#setting motor directions
IO.output(leftMotorDirPin1, 1)
IO.output(leftMotorDirPin2, 0)
IO.output(rightMotorDirPin1, 1)
IO.output(rightMotorDirPin2, 0)




#setting pwm frequency for each pin
motorPWM1 = IO.PWM(leftMotorEnPin, motorsPWMFrequency)
motorPWM2 = IO.PWM(rightMotorEnPin, motorsPWMFrequency)



motorPWM1.start(motorSpeed)
motorPWM2.start(motorSpeed)
motorPWM2.ChangeDutyCycle(10)
time.sleep(5)

'''
for i in range(20):
    motorSpeed += 5
    motorPWM1.ChangeDutyCycle(motorSpeed)
    motorPWM2.ChangeDutyCycle(motorSpeed)
    time.sleep(0.05)
for i in range(20):
    motorSpeed -= 5
    motorPWM1.ChangeDutyCycle(motorSpeed)
    motorPWM2.ChangeDutyCycle(motorSpeed)
    time.sleep(0.05)
    
motorPWM1.stop()
motorPWM2.stop()
'''

IO.cleanup()