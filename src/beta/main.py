from mouse import *
import time
mouse = Mouse()


def run_for(function, delay):
    count = 0
    last_time = time.time()
    while (time.time() - last_time < delay):
        function()
        count += 1
    print("Count ", count)


def move_forward():
    mouse.move_with_pid(Motor.FORWARD)


# run_for(mouse.get_distances, 10)
# run_for(mouse.move_forwards, 3.5)
run_for(mouse.read_bearing, 10)
# run_for(mouse.read_bearing_with_motor, 2)
# mouse.stop_moving()
# run_for(mouse.read_bearing, 2)
# run_for(mouse.read_bearing_with_motor, 2)
# mouse.stop_moving()

# run_for(move_forward, 2.5)



# mouse.go_straight()
# time.sleep(0.8)

# mouse.turn_left()

# mouse.move_foward_steps(1)

mouse.shutdown()
