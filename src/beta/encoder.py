import RPi.GPIO as IO
import time


class Encoder:
    def __init__(self, ENCODER_PIN):
        self.ENCODER_PIN = ENCODER_PIN
        self.debounce_time = 0.035
        self.distance_per_count = 2.522 * 10

        # setting the mode how to read the pins
        IO.setmode(IO.BOARD)
        IO.setup(ENCODER_PIN, IO.IN)

        self.counter = 0
        self.last_time = time.time()

        IO.add_event_detect(ENCODER_PIN, IO.RISING)
        IO.add_event_callback(ENCODER_PIN, self.increment)

    def increment(self, channel):
        if ((time.time() - self.last_time) > self.debounce_time):
            self.counter += 1
            self.last_time = time.time()

    def reset_distance(self):
        self.counter = 0

    def get_distance(self):
        return self.distance_per_count * self.counter
