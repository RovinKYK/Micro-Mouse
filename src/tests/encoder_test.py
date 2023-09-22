import RPi.GPIO as IO
import time

# variables
encoderPin = 29
leftMotorEnPin = 11
rightMotorEnPin = 13
leftMotorDirPin1 = 15
leftMotorDirPin2 = 19
rightMotorDirPin1 = 21
rightMotorDirPin2 = 23

motorsPWMFrequency = 256
motorSpeed = 0

#setting the mode how to read the pins
IO.setmode(IO.BOARD)
IO.setup(leftMotorEnPin, IO.OUT)
IO.setup(rightMotorEnPin, IO.OUT)
IO.setup(leftMotorDirPin1, IO.OUT)
IO.setup(leftMotorDirPin2, IO.OUT)
IO.setup(rightMotorDirPin1, IO.OUT)
IO.setup(rightMotorDirPin2, IO.OUT)
IO.setup(encoderPin, IO.IN)

IO.output(leftMotorDirPin1, 0)
IO.output(leftMotorDirPin2, 1)
IO.output(rightMotorDirPin1, 1)
IO.output(rightMotorDirPin2, 0)


counter = 0
lastSec = time.time()
def increment(channel):
    global counter, lastSec
    if ((time.time() - lastSec) > 0.035):
        counter += 1
        lastSec = time.time()
    
IO.add_event_detect(encoderPin, IO.RISING)
IO.add_event_callback(encoderPin, increment)

motorPWM1 = IO.PWM(leftMotorEnPin, motorsPWMFrequency)
motorPWM2 = IO.PWM(rightMotorEnPin, motorsPWMFrequency)

time.sleep(2)

# Start
try:
    motorPWM1.start(motorSpeed)
    motorPWM2.start(motorSpeed)

    for speed in range(8, 9): 
        motorPWM1.ChangeDutyCycle(speed)
        motorPWM2.ChangeDutyCycle(speed)
        time.sleep(3)

    print(counter)
except KeyboardInterrupt:
    print("Interrupted")
finally:
    IO.cleanup()
    motorPWM1.stop()
    motorPWM2.stop()