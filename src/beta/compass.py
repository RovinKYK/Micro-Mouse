from QMC5883L import *
import time

class Compass:
    def __init__(self):
        time.sleep(1)
        self.sensor = QMC5883L(output_data_rate=ODR_100HZ)
        time.sleep(1)

        self.sensor.declination = -2.11
        self.offset = 0
        self.orientation = 'N'

    def reset_bearing(self):
        self.offset = self.get_true_bearing()
        self.orientation = 'N'

    def get_orientation(self, bearing):
        print(bearing)
        if (45 <= bearing <= 135):
            self.orientation = 'E'
        elif (135 <= bearing <= 225):
            self.orientation = 'S'
        elif (225 <= bearing <= 315):
            self.orientation = 'W'
        else:
            self.orientation = 'N'
        return  self.orientation

    def get_bearing(self):
        true_bearing = self.get_true_bearing()
        if (true_bearing):
            relative_bearing = true_bearing - self.offset
            if relative_bearing < 0:
                relative_bearing = 360 + relative_bearing
                
            return relative_bearing
        return None

    def get_true_bearing(self):
        return self.sensor.get_bearing()