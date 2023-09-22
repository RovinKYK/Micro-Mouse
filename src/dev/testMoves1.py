<<<<<<< HEAD
from mouse import *
import time
from compass import *

mouse = Mouse()
mouse.shutdown()
compass = Compass()

try:
    for i in range(50):
        #mouse.move_forwards()
        #print(compass.get_true_bearing())
        time.sleep(0.1)
    print("Starting turn right")
    mouse.turn_right()
    print("Done turning right")

except KeyboardInterrupt:
    pass
finally:
    mouse.shutdown()

=======
from mouse import *
import time
from compass import *
mouse = Mouse()
compass = Compass()

try:
    for i in range(50):
        mouse.move_forwards()
        print(compass.get_true_bearing())
        time.sleep(0.1)
    print("Starting turn right")
    mouse.turn_right()
    print("Done turning right")


except KeyboardInterrupt:
    pass
finally:
    mouse.shutdown()

>>>>>>> 54be1ffd3e414474858a7b87f1eae1a760388cab
