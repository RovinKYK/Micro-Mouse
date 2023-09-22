from math import sin, radians
import RPi.GPIO as IO
from pid import pid_controller
from pins import *
from address_map import *
from offset_map import *
from motor import Motor
from distance_sensor import DistanceSensor
from compass import Compass
from encoder import Encoder


class Mouse:
    WALL_DETECT_DISTANCE = 100
    TURN_SPEED = 20
    STEP_DISTANCE = 140
    FRONT_WALL_STOP_DISTANCE = 10

    def __init__(self):
        self.left_motor = Motor(
            LEFT_MOTOR_EN_PIN, LEFT_MOTOR_DIR_PIN1, LEFT_MOTOR_DIR_PIN2)
        self.right_motor = Motor(
            RIGHT_MOTOR_EN_PIN, RIGHT_MOTOR_DIR_PIN1, RIGHT_MOTOR_DIR_PIN2)

        self.front_distance_sensor = DistanceSensor(
            FRONT_DIST_SENSOR_PIN, FRONT_DIST_SENSOR_ADDR, FRONT_DIST_SENSOR_OFFSET)
        self.left_distance_sensor = DistanceSensor(
            LEFT_DIST_SENSOR_PIN, LEFT_DIST_SENSOR_ADDR, LEFT_DIST_SENSOR_OFFSET)
        self.right_distance_sensor = DistanceSensor(
            RIGHT_DIST_SENSOR_PIN, RIGHT_DIST_SENSOR_ADDR, RIGHT_DIST_SENSOR_OFFSET)
        self.left_angle_distance_sensor = DistanceSensor(
            FRONT_LEFT_DIST_SENSOR_PIN, FRONT_LEFT_DIST_SENSOR_ADDR, FRONT_LEFT_DIST_SENSOR_OFFSET)
        self.right_angle_distance_sensor = DistanceSensor(
            FRONT_RIGHT_DIST_SENSOR_PIN, FRONT_RIGHT_DIST_SENSOR_ADDR, FRONT_RIGHT_DIST_SENSOR_OFFSET)
        self.back_distance_sensor = DistanceSensor(
            BACK_DIST_SENSOR_PIN, BACK_DIST_SENSOR_ADDR, BACK_DIST_SENSOR_OFFSET)

        self.compass = Compass()
        self.encoder = Encoder(ENCODER_PIN)

        self.front_distance_sensor.start()
        self.back_distance_sensor.start()
        self.left_distance_sensor.start()
        self.right_distance_sensor.start()
        self.compass.reset_bearing()
        self.encoder.reset_distance()

        self.orientation = 'N'

    def move_with_pid(self, direction):
        self.left_motor.setDirection(direction)
        self.right_motor.setDirection(direction)

        left_distance = self.left_distance_sensor.get_distance()
        right_distance = self.right_distance_sensor.get_distance()
        error = left_distance - right_distance
        print(left_distance, right_distance, error)

        left_speed, right_speed = pid_controller(error)
        print(left_speed, right_speed, "\n")

        self.left_motor.setMotorSpeed(left_speed)
        self.right_motor.setMotorSpeed(right_speed)

        self.left_motor.move()
        self.right_motor.move()

    def move_with_pid2(self, direction):
        self.left_motor.setDirection(direction)
        self.right_motor.setDirection(direction)

        left_distance = self.left_distance_sensor.get_distance()
        right_distance = self.right_distance_sensor.get_distance()
        distance_error = left_distance - right_distance
        angle_error = sin(radians(self.compass.get_bearing()))

        error = 1 * distance_error + 30 * angle_error
        print(distance_error, 30 * angle_error, error)

        left_speed, right_speed = pid_controller(error)
        print(left_speed, right_speed, "\n")

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
        self.encoder.reset_distance()
        wheel_distance = 0
        while (wheel_distance <= steps * Mouse.STEP_DISTANCE):
            self.move_with_pid2(Motor.FORWARD)
            wheel_distance = self.encoder.get_distance()

            front_distance = self.front_distance_sensor.get_distance()
            print("Wheel Distance", wheel_distance,
                  "Front Distance", front_distance)
            if (front_distance <= Mouse.FRONT_WALL_STOP_DISTANCE):
                break
        self.brake()
        self.stop_moving()

    def move_backward_steps(self, steps):
        self.encoder.reset_distance()
        distance = 0
        while (distance <= steps * Mouse.STEP_DISTANCE):
            self.move_with_pid(Motor.BACKWARD)
            distance = self.encoder.get_distance()
            # if (self.front_distance_sensor.get_distance() <= Mouse.FRONT_WALL_STOP_DISTANCE):
            #     break

        self.stop_moving()

    def walls(self):
        return self.is_left_wall_present(), self.is_front_wall_present(), self.is_right_wall_present()

    def is_left_wall_present(self):
        return self.left_distance_sensor.get_distance() > Mouse.WALL_DETECT_DISTANCE

    def is_right_wall_present(self):
        return self.right_distance_sensor.get_distance() > Mouse.WALL_DETECT_DISTANCE

    def is_front_wall_present(self):
        return self.front_distance_sensor.get_distance() > Mouse.WALL_DETECT_DISTANCE

    def turn_right(self):
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
            angle_to_turn = expected_bearing - self.compass.get_bearing()
            if angle_to_turn < 0:
                angle_to_turn += 360
            return not (0 <= angle_to_turn <= 10)

        while (should_turn(expected_bearing)):
            self.left_motor.move()
            self.right_motor.move()

        self.left_motor.stopMoving()
        self.right_motor.stopMoving()

    def turn_left(self):
        self.left_motor.setDirection(Motor.BACKWARD)
        self.right_motor.setDirection(Motor.FORWARD)
        self.left_motor.setMotorSpeed(Mouse.TURN_SPEED)
        self.right_motor.setMotorSpeed(Mouse.TURN_SPEED)

        orientation = self.compass.get_orientation()
        print("Start Orientation", orientation)
        if orientation == 'N':
            expected_bearing = 270
        elif orientation == 'E':
            expected_bearing = 0
        elif orientation == 'S':
            expected_bearing = 90
        else:
            expected_bearing = 180

        def should_turn(expected_bearing):
            current_bearing = self.compass.get_bearing()
            angle_to_turn = current_bearing - expected_bearing
            # print(self.compass.get_bearing(), expected_bearing)
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
        IO.cleanup()
        self.left_motor.shutdown()
        self.right_motor.shutdown()

    # Functions below this line are used for testing purposes

    def get_side_distances(self):
        left_distance = self.left_distance_sensor.get_distance()
        right_distance = self.right_distance_sensor.get_distance()
        error = left_distance - right_distance
        print(left_distance, right_distance, error)

    def get_head_distances(self):
        front_distance = self.front_distance_sensor.get_distance()
        back_distance = self.back_distance_sensor.get_distance()
        print(front_distance, back_distance)

    def read_bearing(self):
        print(self.compass.get_bearing())

    def read_bearing_with_motor(self):
        self.left_motor.setDirection(Motor.FORWARD)
        self.left_motor.setMotorSpeed(15)
        self.left_motor.move()

        print(self.compass.get_bearing())

    def go_straight(self):
        self.left_motor.setDirection(Motor.FORWARD)
        self.right_motor.setDirection(Motor.FORWARD)
        self.left_motor.setMotorSpeed(25)
        self.right_motor.setMotorSpeed(30)

        self.left_motor.move()
        self.right_motor.move()
