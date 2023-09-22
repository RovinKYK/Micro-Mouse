import threading
import RPi.GPIO as IO
from pid import *
from constants import *
from motor import Motor
from distance_sensor import DistanceSensor
from compass import Compass
from encoder import Encoder


class Mouse:
    WALL_DETECT_DISTANCE = 100
    TURN_SPEED = 20
    STEP_DISTANCE = 140
    WALL_STOP_DISTANCE = 15
    MAX_RELIABLE_DISTANCE = 400

    def __init__(self):
        print("Initializing micro mouse")
        IO.setmode(IO.BOARD)
        IO.setup(YELLOW_LED1_PIN, IO.OUT)
        IO.setup(RED_LED_PIN, IO.OUT)
        IO.output(YELLOW_LED1_PIN, IO.HIGH)

        self.left_motor = Motor(
            LEFT_MOTOR_EN_PIN, LEFT_MOTOR_DIR_PIN1, LEFT_MOTOR_DIR_PIN2)
        self.right_motor = Motor(
            RIGHT_MOTOR_EN_PIN, RIGHT_MOTOR_DIR_PIN1, RIGHT_MOTOR_DIR_PIN2)

        self.front_distance_sensor = DistanceSensor(
            FRONT_DIST_SENSOR_PIN, FRONT_DIST_SENSOR_BUS, FRONT_DIST_SENSOR_OFFSET)
        self.left_distance_sensor = DistanceSensor(
            LEFT_DIST_SENSOR_PIN, LEFT_DIST_SENSOR_BUS, LEFT_DIST_SENSOR_OFFSET)
        self.right_distance_sensor = DistanceSensor(
            RIGHT_DIST_SENSOR_PIN, RIGHT_DIST_SENSOR_BUS, RIGHT_DIST_SENSOR_OFFSET)
        self.back_distance_sensor = DistanceSensor(
            BACK_DIST_SENSOR_PIN, BACK_DIST_SENSOR_BUS, BACK_DIST_SENSOR_OFFSET)

        self.compass = Compass()
        self.encoder = Encoder(ENCODER_PIN)

        self.front_distance_sensor.start()
        self.left_distance_sensor.start()
        self.right_distance_sensor.start()
        self.back_distance_sensor.start()
        
        self.compass.reset_bearing()
        self.encoder.reset_distance()

        # self.bearing = self.compass.get_bearing()
        # self.orientation = self.compass.get_orientation(self.bearing)
        self.bearing = 0
        self.orientation = 'N'
        
        # print(self.bearing, self.orientation)

        self.front_distance = self.front_distance_sensor.get_distance()
        self.right_distance = self.right_distance_sensor.get_distance()
        self.left_distance = self.left_distance_sensor.get_distance()
        self.back_distance = self.back_distance_sensor.get_distance()

        threading.Thread(target=self.update_front_distance, daemon=True).start()
        threading.Thread(target=self.update_right_distance, daemon=True).start()
        threading.Thread(target=self.update_left_distance, daemon=True).start()
        threading.Thread(target=self.update_back_distance, daemon=True).start()
        threading.Thread(target=self.update_bearing, daemon=True).start()

        IO.output(YELLOW_LED1_PIN, IO.LOW)
        IO.output(RED_LED_PIN, IO.LOW)
        print("Finished initialization")

    def update_front_distance(self):
        while True:
            self.front_distance = self.front_distance_sensor.get_distance()

    def update_right_distance(self):
        while True:
            self.right_distance = self.right_distance_sensor.get_distance()

    def update_left_distance(self):
        while True:
            self.left_distance = self.left_distance_sensor.get_distance()

    def update_back_distance(self):
        while True:
            self.back_distance = self.back_distance_sensor.get_distance()

    def update_bearing(self):
        while True:
            bearing = self.compass.get_bearing()
            if (bearing):
                self.bearing = bearing
                self.orientation = self.compass.get_orientation(bearing)
            time.sleep(0.01)

    def move_with_pid(self, direction):
        self.left_motor.setDirection(direction)
        self.right_motor.setDirection(direction)

        error = calculate_error(self.left_distance, self.right_distance, self.bearing, self.orientation)
        left_speed, right_speed = pid_controller(error)
        # print(left_speed, right_speed, "\n")

        self.left_motor.setMotorSpeed(left_speed)
        self.right_motor.setMotorSpeed(right_speed)

        self.left_motor.move()
        self.right_motor.move()

    def brake(self):
        self.left_motor.setDirection(Motor.LOCK)
        self.right_motor.setDirection(Motor.LOCK)

    def stop_moving(self):
        self.left_motor.stopMoving()
        self.right_motor.stopMoving()

    def move_foward_steps(self, steps):
        print("Moving foward", steps, "steps")
        self.encoder.reset_distance()
        init_front_adj_distance = self.front_distance * math.cos(math.radians(self.divergent_angle()))

        def check_if_should_move():
            if (self.front_distance < Mouse.MAX_RELIABLE_DISTANCE):
                front_adj_distance = self.front_distance * math.cos(math.radians(self.divergent_angle()))
                return (init_front_adj_distance - front_adj_distance <= steps * 148)
            else:
                wheel_distance = self.encoder.get_distance()
                return (wheel_distance <= steps * Mouse.STEP_DISTANCE)

        while (check_if_should_move()):
            self.move_with_pid(Motor.FORWARD)
            if (self.front_distance <= Mouse.WALL_STOP_DISTANCE):
                break

        self.stop_moving()

    def move_backward_steps(self, steps):
        print("Moving backward", steps, "steps")

        self.encoder.reset_distance()
        init_back_adj_distance = self.back_distance * math.cos(math.radians(self.divergent_angle()))

        def check_if_should_move():
            if (self.back_distance < Mouse.MAX_RELIABLE_DISTANCE):
                back_adj_distance = self.back_distance * math.cos(math.radians(self.divergent_angle()))
                return (init_back_adj_distance - back_adj_distance <= steps * 148)
            else:
                wheel_distance = self.encoder.get_distance()
                return (wheel_distance <= steps * Mouse.STEP_DISTANCE)

        while (check_if_should_move()):
            self.move_with_pid(Motor.BACKWARD)
            if (self.back_distance <= Mouse.WALL_STOP_DISTANCE):
                break
        self.stop_moving()

    def divergent_angle(self):
        angle = 0
        if self.orientation == "N":
            if (self.bearing >270):
                angle = self.bearing-360
            else:
                angle = self.bearing
        elif self.orientation == "E":
            angle = self.bearing-90
        elif self.orientation == "S":
            angle = self.bearing-180
        elif self.orientation == "W":
            angle = self.bearing-270
        return angle

    def is_left_wall_present(self):
        return self.left_distance < Mouse.WALL_DETECT_DISTANCE

    def is_right_wall_present(self):
        return self.right_distance < Mouse.WALL_DETECT_DISTANCE

    def is_front_wall_present(self):
        return self.front_distance < Mouse.WALL_DETECT_DISTANCE

    def turn_right(self):
        print("Turning right")
        self.left_motor.setDirection(Motor.FORWARD)
        self.right_motor.setDirection(Motor.BACKWARD)
        self.left_motor.setMotorSpeed(Mouse.TURN_SPEED)
        self.right_motor.setMotorSpeed(Mouse.TURN_SPEED)

        orientation = self.compass.get_orientation()
        if orientation == 'N':
            expected_bearing = 90
        elif orientation == 'E':
            expected_bearing = 180
        elif orientation == 'S':
            expected_bearing = 270
        else:
            expected_bearing = 360

        def should_turn(expected_bearing):
            angle_to_turn = expected_bearing - self.bearing
            if angle_to_turn < 0:
                angle_to_turn += 360
            return not (0 <= angle_to_turn <= 10)

        while (should_turn(expected_bearing)):
            self.left_motor.move()
            self.right_motor.move()

        self.left_motor.stopMoving()
        self.right_motor.stopMoving()

    def turn_left(self):
        print("Turning left")
        self.left_motor.setDirection(Motor.BACKWARD)
        self.right_motor.setDirection(Motor.FORWARD)
        self.left_motor.setMotorSpeed(Mouse.TURN_SPEED)
        self.right_motor.setMotorSpeed(Mouse.TURN_SPEED)

        orientation = self.compass.get_orientation()
        if orientation == 'N':
            expected_bearing = 270
        elif orientation == 'E':
            expected_bearing = 0
        elif orientation == 'S':
            expected_bearing = 90
        else:
            expected_bearing = 180

        def should_turn(expected_bearing):
            current_bearing = self.bearing
            angle_to_turn = current_bearing - expected_bearing
            # print(self.bearing, expected_bearing)
            if angle_to_turn < 0:
                angle_to_turn += 360
            print(current_bearing, angle_to_turn)
            return not (0 <= angle_to_turn <= 10)

        while (should_turn(expected_bearing)):
            self.left_motor.move()
            self.right_motor.move()

        self.left_motor.stopMoving()
        self.right_motor.stopMoving()

    def shutdown(self):
        self.front_distance_sensor.stop()
        self.left_distance_sensor.stop()
        self.right_distance_sensor.stop()
        self.back_distance_sensor.stop()

        self.left_motor.shutdown()
        self.right_motor.shutdown()
        IO.cleanup()


    # Functions below this line are used for testing purposes

    def get_distances(self):
        print(self.left_distance, self.right_distance, self.front_distance, self.back_distance)

    def read_bearing(self):
        print(self.bearing)

    def read_bearing_with_motor(self):
        self.left_motor.setDirection(Motor.FORWARD)
        self.left_motor.setMotorSpeed(15)
        self.left_motor.move()

        print(self.bearing)

    def go_straight(self):
        self.left_motor.setDirection(Motor.FORWARD)
        self.right_motor.setDirection(Motor.FORWARD)
        self.left_motor.setMotorSpeed(25)
        self.right_motor.setMotorSpeed(30)

        self.left_motor.move()
        self.right_motor.move()
