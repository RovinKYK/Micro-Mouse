import libraries.qmc5883l
import time

sensor = qmc5883l.QMC5883L()
sensor.declination = -2.0167
for i in range(0, 10000):
    b = sensor.get_bearing()
    print(b)
    time.sleep(0.01)