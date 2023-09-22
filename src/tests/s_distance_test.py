import time
import VL53L0X
import RPi.GPIO as GPIO

front_x = 12
front_right_x = 8
front_left_x = 38
left_x = 36
right_x = 10
back_x = 40

current = right_x

GPIO.setwarnings(False)

# Setup GPIO for shutdown pins on each VL53L0X
GPIO.setmode(GPIO.BOARD)
GPIO.setup(front_x, GPIO.OUT)
GPIO.setup(front_right_x, GPIO.OUT)
GPIO.setup(front_left_x, GPIO.OUT)
GPIO.setup(left_x, GPIO.OUT)
GPIO.setup(right_x, GPIO.OUT)
GPIO.setup(back_x, GPIO.OUT)

# Set all shutdown pins low to turn off each VL53L0X
GPIO.output(front_x, GPIO.LOW)
GPIO.output(front_right_x, GPIO.LOW)
GPIO.output(front_left_x, GPIO.LOW)
GPIO.output(left_x, GPIO.LOW)
GPIO.output(right_x, GPIO.LOW)
GPIO.output(back_x, GPIO.LOW)

# Keep all low for 500 ms or so to make sure they reset
time.sleep(0.50)

# Create one object per VL53L0X passing the address to give to
# each.
tof = VL53L0X.VL53L0X(address=0x2B)

# Set shutdown pin high for the first VL53L0X then 
# call to start ranging 
GPIO.output(current, GPIO.HIGH)
time.sleep(0.50)

tof.start_ranging(VL53L0X.VL53L0X_BEST_ACCURACY_MODE)

timing = tof.get_timing()
if (timing < 20000):
    timing = 20000
print ("Timing %d ms" % (timing/1000))

for count in range(1,10000):
    distance = tof.get_distance()
    #if (distance > 0):
    print ("sensor %d - %d mm, %d cm, iteration %d" % (tof.my_object_number, distance, (distance/10), count))
    #else:
    #    print ("%d - Error" % tof.my_object_number)
    
    time.sleep(timing/500000.00)

GPIO.output(current, GPIO.LOW)
tof.stop_ranging()


