import RPi.GPIO as IO
from adafruit_extended_bus import ExtendedI2C as I2C
import busio
import adafruit_vl53l0x
import time

class DistanceSensor:
    def __init__(self, reset_pin, i2c_bus, offset):
        self.reset_pin = reset_pin
        self.offset = offset
        self.i2c_bus = i2c_bus
        self.MAX_DISTANCE = 1000

        IO.setmode(IO.BOARD)
        IO.setup(self.reset_pin, IO.OUT)
        IO.output(self.reset_pin, IO.LOW)
        time.sleep(0.5)        

    def start(self):
        IO.output(self.reset_pin, IO.HIGH)
        time.sleep(0.5)

        i2c = I2C(self.i2c_bus)
        self.vl53 = adafruit_vl53l0x.VL53L0X(i2c)
        self.vl53.measurement_timing_budget = 20000
        self.vl53.start_continuous()

    def get_distance(self):
        distance = self.vl53.range + self.offset
        if distance > self.MAX_DISTANCE:
            distance = self.MAX_DISTANCE
        if distance < 0:
            distance = 0
        return distance

    def stop(self):
        self.vl53.stop_continuous()