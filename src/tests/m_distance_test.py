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

IO.output(current, IO.HIGH)
time.sleep(0.50)
tofFrontSensor.start_ranging(VL53L0X.VL53L0X_BSET_ACCURACY_MODE)
IO.output(current, IO.LOW)
tofFrontSensor.stop_ranging()

# FrontLeft Sensor
currentSensor = FrontLeftSensorPin
IO.output(current, IO.HIGH)
time.sleep(0.50)
tofFrontLeftSensor.start_ranging(VL53L0X.VL53L0X_BSET_ACCURACY_MODE)
IO.output(current, IO.LOW)
tofFrontLeftSensor.stop_ranging()

# FrontRight Sensor
currentSensor = FrontRightSensorPin
IO.output(current, IO.HIGH)
time.sleep(0.50)
tofFrontRightSensor.start_ranging(VL53L0X.VL53L0X_BSET_ACCURACY_MODE)
IO.output(current, IO.LOW)
tofFrontRightSensor.stop_ranging()

# Back Sensor
currentSensor = BackSensorPin
IO.output(current, IO.HIGH)
time.sleep(0.50)
tofBackSensor.start_ranging(VL53L0X.VL53L0X_BSET_ACCURACY_MODE)
IO.output(current, IO.LOW)
tofBackSensor.stop_ranging()

# BackLeft Sensor
currentSensor = BackLeftSensorPin
IO.output(current, IO.HIGH)
time.sleep(0.50)
tofBackLeftSensor.start_ranging(VL53L0X.VL53L0X_BSET_ACCURACY_MODE)
IO.output(current, IO.LOW)
tofBackLeftSensor.stop_ranging()

# BackRight Sensor
currentSensor = BackRightSensorPin
IO.output(current, IO.HIGH)
time.sleep(0.50)
tofBackRightSensor.start_ranging(VL53L0X.VL53L0X_BSET_ACCURACY_MODE)
IO.output(current, IO.LOW)
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
print("BL : Timing %d ms" % (timing/1000))

timing = tofBackRightSensor.get_timing()
if (timing < 20000):
    timing = 20000
print("BR : Timing %d ms" % (timing/1000))



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
            distanceBF = tofBackRightSensor.get_distance()

            print("Iteration : %d" % count)
            print("Sensor %d - %d mm, %d cm" % (tof.my_object_number, distanceF, (distanceF / 10)))
            print("Sensor %d - %d mm, %d cm" % (tof.my_object_number, distanceFL, (distanceFL / 10)))
            print("Sensor %d - %d mm, %d cm" % (tof.my_object_number, distanceFR, (distanceFR / 10)))
            print("Sensor %d - %d mm, %d cm" % (tof.my_object_number, distanceB, (distanceB / 10)))
            print("Sensor %d - %d mm, %d cm" % (tof.my_object_number, distanceBL, (distanceBL / 10)))
            print("Sensor %d - %d mm, %d cm" % (tof.my_object_number, distanceBR, (distanceBR / 10)))
            print("\n\n")

            time.sleep(timing / 100000.00)

    def getOneSensorReading(self, sensorName):
        print(sensorName)

        if (sensorName == "F"):
            print(tofFrontSensor.get_distance())
        elif (sensorName == "FL"):
            print(tofFrontLeftSensor.get_distance())
        elif (sensorName == "FR"):
            print(tofFrontRightSensor.get_distance())
        elif (sensorName == "B"):
            print(tofBackSensor.get_distance())
        elif (sensorName == "BL"):
            print(tofBackLeftSensor.get_distance())
        elif (sensorName == "BR"):
            print(tofBackRightSensor.get_distance())

    def getAutoOneSensorReading(self, sensorName):
        for count in range(1, 100000):
            print("Iteration : %d" % count)
            getOneSensorReading(sensorName)
            print("\n\n")

            time.sleep(timing / 100000.00)


mySensors = Sensors()
mySensors.getAutoDetailedAllSensorReadings()