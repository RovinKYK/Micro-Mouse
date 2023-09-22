import time
import VL53L0X
import RPi.GPIO as IO
# from fake_rpi.RPi import GPIO as IO


frontSensorPin = 12
frontRightSensorPin = 8
frontLeftSensorPin = 38
backSensorPin = 36
backRightSensorPin = 10
backLeftSensorPin = 40


IO.setwarnings(False)

# setting board pin read mode
IO.setmode(IO.BOARD)

# setting pins as I/O
IO.setup(frontSensorPin, IO.OUT)
IO.setup(frontRightSensorPin, IO.OUT)
IO.setup(frontLeftSensorPin, IO.OUT)
IO.setup(backSensorPin, IO.OUT)
IO.setup(backRightSensorPin, IO.OUT)
IO.setup(backLeftSensorPin, IO.OUT)


# set all shutdown pins low to turn off each sensor
IO.output(frontSensorPin, IO.LOW)
IO.output(frontLeftSensorPin, IO.LOW)
IO.output(frontRightSensorPin, IO.LOW)
IO.output(backSensorPin, IO.LOW)
IO.output(backLeftSensorPin, IO.LOW)
IO.output(backRightSensorPin, IO.LOW)

time.sleep(0.50)

# create tof objects
tofFrontSensor = VL53L0X.VL53L0X(address = 0x20)
tofFrontLeftSensor = VL53L0X.VL53L0X(address = 0x21)
tofFrontRightSensor = VL53L0X.VL53L0X(address = 0x22)
tofBackSensor = VL53L0X.VL53L0X(address = 0x23)
tofBackLeftSensor = VL53L0X.VL53L0X(address = 0x24)
tofBackRightSensor = VL53L0X.VL53L0X(address = 0x25)



# Assigning addresses
###############################################################################################

# front Sensor
currentSensor = frontSensorPin
IO.output(currentSensor, IO.HIGH)
time.sleep(0.50)
tofFrontSensor.start_ranging(VL53L0X.VL53L0X_BEST_ACCURACY_MODE)
IO.output(currentSensor, IO.LOW)
tofFrontSensor.stop_ranging()

# FrontLeft Sensor
currentSensor = frontLeftSensorPin
IO.output(currentSensor, IO.HIGH)
time.sleep(0.50)
tofFrontLeftSensor.start_ranging(VL53L0X.VL53L0X_BEST_ACCURACY_MODE)
IO.output(currentSensor, IO.LOW)
tofFrontLeftSensor.stop_ranging()

# FrontRight Sensor
currentSensor = frontRightSensorPin
IO.output(currentSensor, IO.HIGH)
time.sleep(0.50)
tofFrontRightSensor.start_ranging(VL53L0X.VL53L0X_BEST_ACCURACY_MODE)
IO.output(currentSensor, IO.LOW)
tofFrontRightSensor.stop_ranging()

# Back Sensor
currentSensor = backSensorPin
IO.output(currentSensor, IO.HIGH)
time.sleep(0.50)
tofBackSensor.start_ranging(VL53L0X.VL53L0X_BEST_ACCURACY_MODE)
IO.output(currentSensor, IO.LOW)
tofBackSensor.stop_ranging()

# BackLeft Sensor
currentSensor = backLeftSensorPin
IO.output(currentSensor, IO.HIGH)
time.sleep(0.50)
tofBackLeftSensor.start_ranging(VL53L0X.VL53L0X_BEST_ACCURACY_MODE)
IO.output(currentSensor, IO.LOW)
tofBackLeftSensor.stop_ranging()

# BackRight Sensor
currentSensor = backRightSensorPin
IO.output(currentSensor, IO.HIGH)
time.sleep(0.50)
tofBackRightSensor.start_ranging(VL53L0X.VL53L0X_BEST_ACCURACY_MODE)
IO.output(currentSensor, IO.LOW)
tofBackRightSensor.stop_ranging()


######################################################################################

# Printing and setting timings

timing = tofFrontSensor.get_timing()
if (timing < 20000):
    timing = 20000
print("F  : Timing %d ms" % (timing/1000))

timing = tofFrontLeftSensor.get_timing()
if (timing < 20000):
    timing = 20000
print("FL : Timing %d ms" % (timing/1000))

timing = tofFrontRightSensor.get_timing()
if (timing < 20000):
    timing = 20000
print("FR : Timing %d ms" % (timing/1000))

timing = tofBackSensor.get_timing()
if (timing < 20000):
    timing = 20000
print("B  : Timing %d ms" % (timing/1000))

timing = tofBackLeftSensor.get_timing()
if (timing < 20000):
    timing = 20000
print("L : Timing %d ms" % (timing/1000))

timing = tofBackRightSensor.get_timing()
if (timing < 20000):
    timing = 20000
print("R : Timing %d ms" % (timing/1000))



class Sensors:
    def getAllSensorsReadings(self):
        print([tofFrontSensor.get_distance(),
               tofFrontLeftSensor.get_distance(),
               tofFrontRightSensor.get_distance(),
               tofBackSensor.get_distance(),
               tofBackLeftSensortofFrontRightSensor.get_distance(),
               tofBackRightSensor.get_distance()])

    def getAutoDetailedAllSensorReadings(self):
        ######################################################################################

        # Taking readings

        for count in range(1, 100000):
            distanceF = tofFrontSensor.get_distance()
            distanceFL = tofFrontLeftSensor.get_distance()
            distanceFR = tofFrontRightSensor.get_distance()
            distanceB = tofBackSensor.get_distance()
            distanceBL = tofBackLeftSensor.get_distance()
            distanceBR = tofBackRightSensor.get_distance()

            print("Iteration : %d" % count)
            print("Sensor %d (F ) - %d mm, %d cm" % (tofFrontSensor.my_object_number, distanceF, (distanceF / 10)))
            print("Sensor %d (FL) - %d mm, %d cm" % (tofFrontLeftSensor.my_object_number, distanceFL, (distanceFL / 10)))
            print("Sensor %d (FR) - %d mm, %d cm" % (tofFrontRightSensor.my_object_number, distanceFR, (distanceFR / 10)))
            print("Sensor %d (B ) - %d mm, %d cm" % (tofBackSensor.my_object_number, distanceB, (distanceB / 10)))
            print("Sensor %d (BL) - %d mm, %d cm" % (tofBackLeftSensor.my_object_number, distanceBL, (distanceBL / 10)))
            print("Sensor %d (BR) - %d mm, %d cm" % (tofBackRightSensor.my_object_number, distanceBR, (distanceBR / 10)))
            print("\n\n")

            time.sleep(timing / 100000.00)


    def getOneSensorReading(self, sensorName):
        print("Sensor :",sensorName)

        if (sensorName == "F"):
            distance = tofFrontSensor.get_distance()
            print(distance)
        elif (sensorName == "FL"):
            distance = tofFrontLeftSensor.get_distance()
            print(distance)
        elif (sensorName == "FR"):
            distance = tofFrontRightSensor.get_distance()
            print(distance)
        elif (sensorName == "B"):
            distance = tofBackSensor.get_distance()
            print(distance)
        elif (sensorName == "L"):
            distance = tofBackLeftSensor.get_distance()
            print(distance)
        elif (sensorName == "R"):
            distance = tofBackRightSensor.get_distance()
            print(distance)


    def getAutoOneSensorReading(self, sensorName):
        for count in range(1, 100000):
            print("Iteration : %d" % count)
            self.getOneSensorReading(sensorName)
            print("\n\n")
            time.sleep(timing / 100000.00)

sensors = Sensors()
Sensors().getAutoDetailedAllSensorReadings()