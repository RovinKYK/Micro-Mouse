from collections import deque
from time import sleep
from mouse import Mouse
import sys
import RPi.GPIO as IO
from constants import *
import traceback


def log(string):
    sys.stderr.write("{}\n".format(string))
    sys.stderr.flush()


class D:
    # Directions
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3
    UNKNOWN = -1
    DIRECTIONS = [0, 1, 2, 3]
    NAMES = ["NORTH", "EAST", "SOUTH", "WEST"]


class Commands:
    FORWARD = 0
    TURN_RIGHT = 1
    GO_BACK = 2
    TURN_LEFT = 3


class Solver:

    def __init__(self, mouse: Mouse):
        # Maze size
        self.LENGTH = 14
        self.mouse = mouse
        # Destination coordinates
        self.DEST_COORDS = ((self.LENGTH // 2, self.LENGTH // 2),)
        self.use_modified = True

        self.floodfill_array = [[float('inf') for i in range(
            self.LENGTH)] for j in range(self.LENGTH)]
        self.dest_x, self.dest_y = self.DEST_COORDS[0]

        self.start_x = 0
        self.start_y = self.LENGTH - 1
        self.start_dir = D.NORTH

        # Assumes the mouse starts in the lower left corner
        # headed towards north.
        # If this assumption is wrong the calculated values
        # will be corrected when enough information is available
        # DONT CHANGE THESE
        self.start_x_rel = 0
        self.start_y_rel = self.LENGTH - 1
        self.start_dir_rel = D.NORTH
        self.orientation_known = False

        self.curr_x = self.start_x_rel
        self.curr_y = self.start_y_rel
        self.prev_x = self.curr_x
        self.prev_y = self.curr_y
        self.front_dir = self.start_dir_rel
        self.detected_walls = [
            [0 for i in range(self.LENGTH)] for j in range(self.LENGTH)]
        self.visited = [[False for i in range(
            self.LENGTH)] for j in range(self.LENGTH)]
        self.fast_run_path = []

    def has_wall(self, dir):
        '''Detect if a wall is present in the current cell in the given
        direction'''

        dir = self.absolute_dir_rel_front(dir)

        if dir == D.NORTH:
            return self.mouse.is_front_wall_present()
        if dir == D.EAST:
            return self.mouse.is_right_wall_present()
        if dir == D.WEST:
            return self.mouse.is_left_wall_present()
        if dir == D.SOUTH:
            # API cannot detect walls in back/
            # Need not detect walls in back
            raise IndexError

    def get_cell(self, x, y, dir):
        '''Get cell in given direction. Returns an invalid coordinate pair if
        out of bounds.'''
        cell = (self.LENGTH, self.LENGTH)
        # Direction.NORTH
        if (dir == D.NORTH and y > 0):
            cell = (x, y - 1)
        # Direction.EAST
        if (dir == D.EAST and x < self.LENGTH - 1):
            return (x + 1, y)
        # Direction.SOUTH
        if (dir == D.SOUTH and y < self.LENGTH - 1):
            return (x, y + 1)
        # Direction.WEST
        if (dir == D.WEST and x > 0):
            return (x - 1, y)

        return cell

    def get_next_dir(self, next_x, next_y):
        '''Get direction of movement to next position'''
        delta_pos = (next_x - self.curr_x, next_y - self.curr_y)
        if delta_pos == (0, -1):
            return D.NORTH
        elif delta_pos == (1, 0):
            return D.EAST
        elif delta_pos == (0, 1):
            return D.SOUTH
        elif delta_pos == (-1, 0):
            return D.WEST
        else:
            return D.UNKNOWN

    def get_next_dir_rel(self, x, y, next_x, next_y):
        '''Get direction of movement to next position relative to given coordinates'''
        delta_pos = (next_x - x, next_y - y)
        if delta_pos == (0, -1):
            return D.NORTH
        elif delta_pos == (1, 0):
            return D.EAST
        elif delta_pos == (0, 1):
            return D.SOUTH
        elif delta_pos == (-1, 0):
            return D.WEST
        else:
            return D.UNKNOWN

    def shift_representation(self):
        '''Mirrors the previous position and current position.
        Moves the first column of cells to the last in the
        detected walls array'''

        # Each wall is represented twice in two cells, so we need to fix it.
        for row in range(self.LENGTH):
            for dir in D.DIRECTIONS:
                if self.check_wall(0, row, dir):
                    self.removeWall(0, row, dir)
                    self.setWall(self.LENGTH - 1, row, dir)

            # Shift visited cells
            self.visited[row].append(self.visited[row].pop(0))

        self.curr_x = self.LENGTH - self.curr_x - 1
        self.prev_x = self.LENGTH - self.prev_x - 1
        self.start_x_rel = self.LENGTH - self.start_x_rel - 1
        # No change to y-coordinates

        # Perform floodfill
        self.floodfill()

    def absolute_dir_rel_start(self, dir):
        '''Get the absolute direction relative to the start direction'''
        return (dir + self.start_dir - self.start_dir_rel) % 4

    def absolute_dir_rel_front(self, dir):
        '''Get the absolute direction relative to the front direction'''
        return (dir - self.front_dir) % 4

    def check_wall(self, x: int, y: int, dir):
        '''Check if wall is present in given direction in the 
        currently explored maze'''
        if dir == D.NORTH:
            return bool(self.detected_walls[y][x] & 1)
        if dir == D.EAST:
            return bool(self.detected_walls[y][x] & 2)
        if dir == D.SOUTH:
            return bool(self.detected_walls[y][x] & 4)
        if dir == D.WEST:
            return bool(self.detected_walls[y][x] & 8)

    def get_adjacent(self, x: int, y: int) -> list[tuple]:
        '''Get coordinates of adjacent cells within bounds'''
        neighbors = []
        # Direction.NORTH
        if y > 0:
            neighbors.append(self.get_cell(x, y, D.NORTH))
        # Direction.EAST
        if x < self.LENGTH - 1:
            neighbors.append(self.get_cell(x, y, D.EAST))
        # Direction.SOUTH
        if y < self.LENGTH - 1:
            neighbors.append(self.get_cell(x, y, D.SOUTH))
        # Direction.WEST
        if x > 0:
            neighbors.append(self.get_cell(x, y, D.WEST))

        return neighbors

    def get_visitable_neighbors(self, x: int, y: int) -> list[tuple]:
        '''Get coordinates of adjacent cells within bounds and
        are not blocked by currently detected walls .'''
        neighbors = []
        # Direction.NORTH
        if y > 0 and not self.check_wall(x, y, D.NORTH):
            neighbors.append(self.get_cell(x, y, D.NORTH))
        # Direction.EAST
        if x < self.LENGTH - 1 and not self.check_wall(x, y, D.EAST):
            neighbors.append(self.get_cell(x, y, D.EAST))
        # Direction.SOUTH
        if y < self.LENGTH - 1 and not self.check_wall(x, y, D.SOUTH):
            neighbors.append(self.get_cell(x, y, D.SOUTH))
        # Direction.WEST
        if x > 0 and not self.check_wall(x, y, D.WEST):
            neighbors.append(self.get_cell(x, y, D.WEST))

        return neighbors

    def get_visited_visitable_neighbors(self, x: int, y: int) -> list[tuple]:
        '''Get coordinates of adjacent cells which were visited within bounds and
        are not blocked by currently detected walls .'''
        neighbors = []
        # Direction.NORTH
        if y > 0 and not self.check_wall(x, y, D.NORTH):
            next_cell = self.get_cell(x, y, D.NORTH)
            if self.visited[next_cell[1]][next_cell[0]]:
                neighbors.append(next_cell)
        # Direction.EAST
        if x < self.LENGTH - 1 and not self.check_wall(x, y, D.EAST) and self.visited[y][x]:
            next_cell = self.get_cell(x, y, D.EAST)
            if self.visited[next_cell[1]][next_cell[0]]:
                neighbors.append(next_cell)
        # Direction.SOUTH
        if y < self.LENGTH - 1 and not self.check_wall(x, y, D.SOUTH) and self.visited[y][x]:
            next_cell = self.get_cell(x, y, D.SOUTH)
            if self.visited[next_cell[1]][next_cell[0]]:
                neighbors.append(next_cell)
        # Direction.WEST
        if x > 0 and not self.check_wall(x, y, D.WEST) and self.visited[y][x]:
            next_cell = self.get_cell(x, y, D.WEST)
            if self.visited[next_cell[1]][next_cell[0]]:
                neighbors.append(next_cell)
        return neighbors

    def floodfill(self, only_visited=False):

        # Reset floodfill array
        self.floodfill_array = [[float('inf') for i in range(
            self.LENGTH)] for j in range(self.LENGTH)]
        queue = deque()
        queue.append([self.dest_x, self.dest_y, 0])

        while queue:
            x, y, new_dist = queue.popleft()
            curr_dist = self.floodfill_array[y][x]

            if only_visited:
                # Only use visited cells to compute floodfill
                neighbors = self.get_visited_visitable_neighbors(x, y)
            else:
                neighbors = self.get_visitable_neighbors(x, y)

            # Check if current distance is less than updated distance
            if (curr_dist <= new_dist):
                continue

            # Update flood value
            self.floodfill_array[y][x] = new_dist

            for neighbor in neighbors:
                queue.append([*neighbor, new_dist + 1])

    def modified_floodfill(self, only_visited=False):
        '''Favor forward direction in flood values'''
        # Reset floodfill array
        self.floodfill_array = [[float('inf') for i in range(
            self.LENGTH)] for j in range(self.LENGTH)]
        queue = deque()
        queue.append([self.dest_x, self.dest_y, 0, D.UNKNOWN])

        x, y = self.dest_x, self.dest_y

        while queue:
            x, y, new_dist, dir = queue.popleft()
            curr_dist = self.floodfill_array[y][x]

            if only_visited:
                # Only use visited cells to compute floodfill
                neighbors = self.get_visited_visitable_neighbors(x, y)
            else:
                neighbors = self.get_visitable_neighbors(x, y)

            # Check if current distance is less than updated distance
            if (curr_dist <= new_dist):
                continue

            # Update flood value

            self.floodfill_array[y][x] = new_dist

            for neighbor in neighbors:
                next_dir = self.get_next_dir_rel(
                    x, y, neighbor[0], neighbor[1])
                if dir == D.UNKNOWN or next_dir == dir:
                    # Unknown direction or next cell is in forward direction
                    queue.append([*neighbor, new_dist + 1, next_dir])
                else:
                    queue.append([*neighbor, new_dist + 3, next_dir])

    def setWall(self, x, y, dir):
        '''Simulates detection of a wall in a direction for the given cell'''
        ox, oy = self.get_cell(x, y, dir)
        try:
            if dir == D.NORTH:
                self.detected_walls[y][x] |= 0b0001
                self.detected_walls[oy][ox] |= 0b0100
            if dir == D.EAST:
                self.detected_walls[y][x] |= 0b0010
                self.detected_walls[oy][ox] |= 0b1000
            if dir == D.SOUTH:
                self.detected_walls[y][x] |= 0b0100
                self.detected_walls[oy][ox] |= 0b0001
            if dir == D.WEST:
                self.detected_walls[y][x] |= 0b1000
                self.detected_walls[oy][ox] |= 0b0010
        except IndexError:
            # The error raised when setting an out of bounds
            # cell can be safely ignored
            pass

    def removeWall(self, x, y, dir):
        '''Removes a wall in a given direction from the detected walls array'''
        ox, oy = self.get_cell(x, y, dir)
        try:
            if dir == D.NORTH:
                self.detected_walls[y][x] ^= 0b0001
                self.detected_walls[oy][ox] ^= 0b1000
            if dir == D.EAST:
                self.detected_walls[y][x] ^= 0b0010
                self.detected_walls[oy][ox] ^= 0b1000
            if dir == D.SOUTH:
                self.detected_walls[y][x] ^= 0b0100
                self.detected_walls[oy][ox] ^= 0b0001
            if dir == D.WEST:
                self.detected_walls[y][x] ^= 0b1000
                self.detected_walls[oy][ox] ^= 0b0010
        except IndexError:
            # The error raised when setting an out of bounds
            # cell can be safely ignored
            pass

    def sense(self):
        '''Simulates sensor retrieval of cell wall information'''
        for dir in D.DIRECTIONS:
            if (self.absolute_dir_rel_front(dir) == D.SOUTH):
                # Can't/Need not detect back walls
                continue
            if self.has_wall(dir):
                self.setWall(self.curr_x, self.curr_y, dir)

        # Perform floodfill
        if self.use_modified:
            self.modified_floodfill()
        else:
            self.floodfill()

    def try_get_wall_on_side(self):
        '''Attempts to figure out orientation from current cell'''
        for dir in [D.EAST, D.WEST]:
            if not self.has_wall(dir):
                return dir
        return D.UNKNOWN

    def try_fix_orientation(self):
        '''Attempts to correct orientation'''
        dir = self.try_get_wall_on_side()
        if dir != D.UNKNOWN:
            if dir == D.EAST:
                pass
                # Current representation is correct
            elif dir == D.WEST:
                # Need to flip orientation
                self.shift_representation()
            self.orientation_known = True

    def visualize_flood_fill_and_visited(self):
        pass
        # for x in range(self.LENGTH):
        #     for y in range(self.LENGTH):
        #         if (self.visited[y][x]):
        #             mouse.setText(x, self.LENGTH - y - 1,
        #                           self.floodfill_array[y][x])
        #             mouse.setColor(x, self.LENGTH - y - 1, 'Y')

    def move(self, dir):
        '''Move the mouse in the given direction. Raises an error if position is
        out of bounds.'''
        self.prev_x = self.curr_x
        self.prev_y = self.curr_y
        self.curr_x, self.curr_y = self.get_cell(self.curr_x, self.curr_y, dir)

        x, y = self.curr_x, self.curr_y
        # Set visit cell
        self.visited[y][x] = True

        orientation = self.absolute_dir_rel_front(dir)
        # Mouse front is in dir
        self.front_dir = dir

        # Forward
        if (orientation == D.NORTH and y >= 0):
            self.mouse.move_foward_steps(1)
        # Right
        elif (orientation == D.EAST and x <= self.LENGTH - 1):
            self.mouse.turn_right()
            self.mouse.move_foward_steps(1)
        # Backward
        elif (orientation == D.SOUTH and y <= self.LENGTH - 1):
            self.mouse.move_backward_steps(1)

        # Left
        elif (orientation == D.WEST and x >= 0):
            self.mouse.turn_left()
            self.mouse.move_foward_steps(1)

        else:
            raise IndexError

    def save_move(self, dir):
        '''Stores the move in fast run path array'''
        self.prev_x = self.curr_x
        self.prev_y = self.curr_y
        self.curr_x, self.curr_y = self.get_cell(self.curr_x, self.curr_y, dir)

        x, y = self.curr_x, self.curr_y

        orientation = self.absolute_dir_rel_front(dir)
        # Mouse front is in dir
        self.front_dir = dir

        # Forward
        if (orientation == D.NORTH and y >= 0):
            self.fast_run_path.append(Commands.FORWARD)
        # Right
        elif (orientation == D.EAST and x <= self.LENGTH - 1):
            self.fast_run_path.append(Commands.TURN_RIGHT)
            self.fast_run_path.append(Commands.FORWARD)
        # Backward
        elif (orientation == D.SOUTH and y <= self.LENGTH - 1):
            self.fast_run_path.append(Commands.TURN_RIGHT)
            self.fast_run_path.append(Commands.TURN_RIGHT)
            self.fast_run_path.append(Commands.FORWARD)
        # Left
        elif (orientation == D.WEST and x >= 0):
            self.fast_run_path.append(Commands.TURN_LEFT)
            self.fast_run_path.append(Commands.FORWARD)

        else:
            raise IndexError

    def search_run(self):
        '''Simulates the search run from starting square to goal'''

        # Set destination
        self.dest_x, self.dest_y = self.DEST_COORDS[0]
        # Sense initial position
        self.sense()

        while True:
            # Destination reached when floodfill value is zero

            if (self.floodfill_array[self.curr_y][self.curr_x] == 0):
                self.visualize_flood_fill_and_visited()
                return 0

            # Unknown start orientation
            if not self.orientation_known:
                self.try_fix_orientation()

            # Move in the direction of lowest floodfill value
            neighbors = self.get_visitable_neighbors(self.curr_x, self.curr_y)

            min_flood_val, next_coord = min(
                ((self.floodfill_array[neighbor[1]][neighbor[0]], neighbor) for neighbor in neighbors))

            next_dir = self.get_next_dir(*next_coord)

            self.move(next_dir)
            self.sense()

    def search_run_back(self, to_start=False):
        '''Simulates the search run from goal to adjacent square of start cell'''

        # Set destination
        if to_start:
            self.dest_x, self.dest_y = self.start_x, self.start_y
        else:
            # Don't go to start square
            self.dest_x, self.dest_y = self.get_visitable_neighbors(
                self.start_x, self.start_y)[0]
        # Sense initial position
        self.sense()

        while True:
            # Destination reached when floodfill value is zero
            if (self.floodfill_array[self.curr_y][self.curr_x] == 0):
                return 0

            # Move in the direction of lowest floodfill value
            neighbors = self.get_visitable_neighbors(self.curr_x, self.curr_y)

            min_flood_val, next_coord = min(
                ((self.floodfill_array[neighbor[1]][neighbor[0]], neighbor) for neighbor in neighbors))

            next_dir = self.get_next_dir(*next_coord)

            self.move(next_dir)
            self.sense()

    def build_fast_run(self):
        '''Stores the fast run path'''

        # Set destination

        self.dest_x, self.dest_y = self.DEST_COORDS[0]

        # Compute final flood values
        if self.use_modified:
            self.modified_floodfill(only_visited=True)
        else:
            self.floodfill(only_visited=True)
        self.visualize_flood_fill_and_visited()

        while True:
            # Destination reached when floodfill value is zero
            if (self.floodfill_array[self.curr_y][self.curr_x] == 0):
                return 0

            # Move in the direction of lowest floodfill value
            neighbors = self.get_visited_visitable_neighbors(
                self.curr_x, self.curr_y)

            min_flood_val, next_coord = min(
                ((self.floodfill_array[neighbor[1]][neighbor[0]], neighbor) for neighbor in neighbors))
            next_dir = self.get_next_dir(*next_coord)
            self.save_move(next_dir)

    def fast_run(self):
        '''Fast run simulation'''
        i = 0
        while i < len(self.fast_run_path):
            a = self.fast_run_path[i]
            if a == Commands.FORWARD:
                # Forward optimization
                forward_steps = 1
                while (i < len(self.fast_run_path) - 1 and self.fast_run_path[i + 1] == Commands.FORWARD):
                    forward_steps += 1
                    i += 1
                print(f"Moving forwards {forward_steps} steps")
                self.mouse.move_foward_steps(forward_steps)

            elif a == Commands.TURN_LEFT:
                print("Turning left")
                self.mouse.turn_left()

            elif a == Commands.TURN_RIGHT:
                print("Turning right")
                self.mouse.turn_right()
            i += 1

    def solve(self):
        print("Search run started")
        self.search_run()
        self.search_run_back(to_start=False)
        self.search_run()
        self.search_run_back(to_start=True)
        print("Fast run started")
        # Fast run
        self.build_fast_run()
        self.fast_run()
        print("Reached destination")


def main():

    mouse = Mouse()
    solver = Solver(mouse)
    solver.solve()



if __name__ == "__main__":
    IO.setmode(IO.BOARD)
    IO.setwarnings(False)
    IO.setup(BUTTON_PIN, IO.IN)
    IO.setup(RED_LED_PIN, IO.OUT)
    
    print("Press button")
    while True:
        if IO.input(BUTTON_PIN):
            IO.output(RED_LED_PIN, IO.LOW)
            try: 
                main()
            except Exception:
                print(traceback.format_exc())
                IO.output(RED_LED_PIN, IO.HIGH)
                IO.cleanup()
                IO.setmode(IO.BOARD)
                IO.setup(BUTTON_PIN, IO.IN)
                IO.setup(RED_LED_PIN, IO.OUT)
 
                sleep(2)