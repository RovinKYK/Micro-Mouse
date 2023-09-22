from mouse import *
import time

mouse = Mouse()


def run_for(function, delay):
    count = 0
    last_time = time.time()
    while time.time() - last_time < delay:
        function()
        count += 1
    print("Count ", count)


def move_forward():
    mouse.move_with_pid2(Motor.FORWARD)


# run_for(mouse.get_side_distances, 10)
# run_for(mouse.move_forwards, 3.5)
# run_for(mouse.read_bearing, 2)
# run_for(mouse.read_bearing_with_motor, 2)
# mouse.stop_moving()
# run_for(mouse.read_bearing, 2)
# run_for(mouse.read_bearing_with_motor, 2)
# mouse.stop_moving()

# run_for(move_forward, 2.5)


# mouse.go_straight()
# time.sleep(0.8)

# mouse.turn_left()

class TestBench:

    def testBench1(self):
        print("Current cell")
        print(mouse.walls())
        print()

        print("Move forward 1 steps")
        mouse.move_foward_steps(1)
        print(mouse.walls())
        print()

        print("Turn Right")
        mouse.turn_right()
        print(mouse.walls())
        print()

        print("Move forward 1 steps")
        mouse.move_foward_steps(1)
        print(mouse.walls())
        print()

    def testBench2(self):
        print("Current cell")
        print(mouse.walls())
        print()

        print("Move forward 1 steps")
        mouse.move_foward_steps(1)
        print(mouse.walls())
        print()

        print("Turn Right")
        mouse.turn_right()
        print(mouse.walls())
        print()

        print("Move forward 1 steps")
        mouse.move_foward_steps(1)
        print(mouse.walls())
        print()

        print("Turn Left")
        mouse.turn_left()
        print(mouse.walls())
        print()

        print("Move forward 1 steps")
        mouse.move_foward_steps(1)
        print(mouse.walls())
        print()

    def testBench3(self):
        print("Current cell")
        print(mouse.walls())
        print()

        print("Move forward 1 steps")
        mouse.move_foward_steps(1)
        print(mouse.walls())
        print()

        print("Turn Right")
        mouse.turn_right()
        print(mouse.walls())
        print()

        print("Move forward 1 steps")
        mouse.move_foward_steps(1)
        print(mouse.walls())
        print()

        print("Turn Right")
        mouse.turn_right()
        print(mouse.walls())
        print()

        print("Move forward 1 steps")
        mouse.move_foward_steps(1)
        print(mouse.walls())
        print()

    def testBench4(self):
        print("Current cell")
        print(mouse.walls())
        print()

        print("Move forward 1 steps")
        mouse.move_foward_steps(1)
        print(mouse.walls())
        print()

        print("Turn Left")
        mouse.turn_left()
        print(mouse.walls())
        print()

        print("Move forward 1 steps")
        mouse.move_foward_steps(1)
        print(mouse.walls())
        print()

        print("Turn Left")
        mouse.turn_left()
        print(mouse.walls())
        print()

        print("Move forward 1 steps")
        mouse.move_foward_steps(1)
        print(mouse.walls())
        print()

        print("Turn Right")
        mouse.turn_right()
        print(mouse.walls())
        print()

        print("Move forward 1 steps")
        mouse.move_foward_steps(1)
        print(mouse.walls())
        print()

        print("Turn Right")
        mouse.turn_right()
        print(mouse.walls())
        print()

        print("Move forward 1 steps")
        mouse.move_foward_steps(1)
        print(mouse.walls())
        print()


mouse.shutdown()
