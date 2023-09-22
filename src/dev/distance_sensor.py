import RPi.GPIO as IO
import VL53L0X
import time

class DistanceSensor:
    def __init__(self, reset_pin, address, offset):
        self.reset_pin = reset_pin
        self.address = address
        self.offset = offset
        self.MAX_DISTANCE = 1000
        
        # IO.setwarnings(False)
        # setting board pin read mode
        IO.setmode(IO.BOARD)
        IO.setup(reset_pin, IO.OUT)

        self.reset()

    def reset(self):
        IO.output(self.reset_pin, IO.LOW)
        time.sleep(0.5)

    def start(self):
        self.sensor = VL53L0X.VL53L0X(address=self.address)
        IO.output(self.reset_pin, IO.HIGH)
        time.sleep(0.5)
        self.sensor.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)

    def get_distance(self):
        distance = self.sensor.get_distance() + self.offset
        if distance > self.MAX_DISTANCE:
            distance = self.MAX_DISTANCE
        if distance < 0:
            distance = 0
        return distance

    def stop(self):
        self.sensor.stop_ranging()
