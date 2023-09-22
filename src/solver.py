from collections import deque


class D:
    # Directions
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3
    UNKNOWN = -1
    DIRECTIONS = [0, 1, 2, 3]
    NAMES = ["NORTH", "EAST", "SOUTH", "WEST"]


class Maze:
    def __init__(self, maze: list[list], start_x: int, start_y: int):
        self.maze = maze
        self.length = len(maze)
        self.start_x = start_x
        self.start_y = start_y
        self.cur_x = self.start_x
        self.cur_y = self.start_y

    def move_pos(self, dir):
        '''Move to cell in given direction. Raises an error if position is
        out of bounds.'''
        x, y = self.cur_x, self.cur_y

        # Direction.NORTH
        if (dir == D.NORTH and y > 0):
            cell = (x, y - 1)
        # Direction.EAST
        elif (dir == D.EAST and x < self.length - 1):
            cell = (x + 1, y)
        # Direction.SOUTH
        elif (dir == D.SOUTH and y < self.length - 1):
            cell = (x, y + 1)
        # Direction.WEST
        elif (dir == D.WEST and x > 0):
            cell = (x - 1, y)
        else:
            raise IndexError

        self.cur_x, self.cur_y = cell

    def has_wall(self, dir):
        '''Detect if a wall is present in the current cell in the given
        direction'''
        x, y = self.cur_x, self.cur_y

        if dir == D.NORTH:
            return bool(self.maze[y][x] & 1)
        if dir == D.EAST:
            return bool(self.maze[y][x] & 2)
        if dir == D.SOUTH:
            return bool(self.maze[y][x] & 4)
        if dir == D.WEST:
            return bool(self.maze[y][x] & 8)

    def get_pos(self):
        return (self.cur_x, self.cur_y)


class Solver:

    def __init__(self, maze: Maze, start_x, start_y, start_dir):
        self.maze = maze
        self.length = maze.length
        self.floodfill_array = [[float('inf') for i in range(
            self.length)] for j in range(self.length)]
        self.dest_x = self.length // 2
        self.dest_y = self.length // 2

        self.start_x = start_x
        self.start_y = start_y
        self.start_dir = start_dir

        # Assumes the mouse starts in the lower left corner
        # headed towards north.
        # If this assumption is wrong the calculated values
        # will be corrected when enough information is available
        # DONT CHANGE THESE
        self.start_x_rel = 0
        self.start_y_rel = self.length - 1
        self.start_dir_rel = D.NORTH
        self.orientation_known = False

        self.curr_x = self.start_x_rel
        self.curr_y = self.start_y_rel
        self.prev_x = self.curr_x
        self.prev_y = self.curr_y
        self.dir = self.start_dir_rel
        self.detected_walls = [
            [0 for i in range(self.length)] for j in range(self.length)]

    def get_cell(self, x, y, dir):
        '''Get cell in given direction. Returns an invalid coordinate pair if
        out of bounds.'''
        cell = (self.length, self.length)
        # Direction.NORTH
        if (dir == D.NORTH and y > 0):
            cell = (x, y - 1)
        # Direction.EAST
        if (dir == D.EAST and x < self.length - 1):
            return (x + 1, y)
        # Direction.SOUTH
        if (dir == D.SOUTH and y < self.length - 1):
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

    def shift_representation(self):
        '''Mirrors the previous position and current position.
        Moves the first column of cells to the last in the
        detected walls array'''

        # Each wall is represented twice in two cells, so we need to fix it.
        for row in range(self.length):
            for dir in D.DIRECTIONS:
                if self.check_wall(0, row, dir):
                    self.removeWall(0, row, dir)
                    self.setWall(self.length - 1, row, dir)

        self.curr_x = self.length - self.curr_x - 1
        self.prev_x = self.length - self.prev_x - 1
        self.start_x_rel = self.length - self.start_x_rel - 1
        # No change to y-coordinates

        # Perform floodfill
        self.floodfill()

    def absolute_dir(self, dir):
        '''Get the absolute direction of the given relative direction'''
        return (dir + self.start_dir - self.start_dir_rel) % 4

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
        if x < self.length - 1:
            neighbors.append(self.get_cell(x, y, D.EAST))
        # Direction.SOUTH
        if y < self.length - 1:
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
        if x < self.length - 1 and not self.check_wall(x, y, D.EAST):
            neighbors.append(self.get_cell(x, y, D.EAST))
        # Direction.SOUTH
        if y < self.length - 1 and not self.check_wall(x, y, D.SOUTH):
            neighbors.append(self.get_cell(x, y, D.SOUTH))
        # Direction.WEST
        if x > 0 and not self.check_wall(x, y, D.WEST):
            neighbors.append(self.get_cell(x, y, D.WEST))

        return neighbors

    def floodfill(self):

        # Reset floodfill array
        self.floodfill_array = [[float('inf') for i in range(
            self.length)] for j in range(self.length)]
        queue = deque()
        queue.append([self.dest_x, self.dest_y, 0])

        while queue:
            x, y, new_dist = queue.popleft()
            curr_dist = self.floodfill_array[y][x]

            neighbors = self.get_visitable_neighbors(x, y)

            # Check if current distance is less than updated distance
            if (curr_dist <= new_dist):
                continue

            # Update flood value
            self.floodfill_array[y][x] = new_dist

            for neighbor in neighbors:
                queue.append([*neighbor, new_dist + 1])

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
            if self.maze.has_wall(self.absolute_dir(dir)):
                self.setWall(self.curr_x, self.curr_y, dir)

        # Perform floodfill
        self.floodfill()

    def get_orientation(self):
        '''Attempts to figure out orientation from current cell'''
        for dir in [D.EAST, D.WEST]:
            if not self.maze.has_wall(self.absolute_dir(dir)):
                return dir
        return D.UNKNOWN

    def fix_orientation(self):
        '''Attempts to correct orientation'''
        dir = self.get_orientation()
        print("Orientation not known. Assuming clockwise orientation")
        if dir != D.UNKNOWN:
            print("Orientation fixed")
            if dir == D.EAST:
                pass
                # print("Current orientation is clockwise")
                # Current representation is correct
            elif dir == D.WEST:
                # Need to flip orientation
                # print("Current orientation is anticlockwise")
                self.shift_representation()
            self.orientation_known = True

    def move(self, x, y):
        '''Simulates movement of mouse.'''
        # Keep track of last coordinate
        self.prev_x = self.curr_x
        self.prev_y = self.curr_y

        self.curr_x = x
        self.curr_y = y

    def run(self):
        '''Simulates the micro mouse'''

        # Sense initial position
        self.sense()
        # print(self.absolute_pos(1, 1))
        # print("Currently at", str((self.curr_x, self.curr_y)), 'rel',
        #       str(self.maze.get_pos()), 'abs')

        while True:
            # break
            # Destination reached when floodfill value is zero
            if (self.floodfill_array[self.curr_y][self.curr_x] == 0):
                print("Reached Destination")
                return 0
            # Unknown start orientation
            if not self.orientation_known:
                self.fix_orientation()

            # print("Currently at", str((self.curr_x, self.curr_y)), 'rel',
            #       str(self.maze.get_pos()), 'abs')

            # print("Detected Walls")
            # print(*self.detected_walls, sep='\n')
            # print("Flood Values")
            # print(*self.floodfill_array, sep='\n')

            # Move in the direction of lowest floodfill value
            neighbors = self.get_visitable_neighbors(self.curr_x, self.curr_y)

            min_flood_val, next_coord = min(
                ((self.floodfill_array[neighbor[1]][neighbor[0]], neighbor) for neighbor in neighbors))

            next_dir = self.get_next_dir(*next_coord)
            # print("Moving to", str(next_coord),
            #       'rel in direction', D.NAMES[next_dir])
            print(D.NAMES[next_dir], end=' ')

            # Update location in maze
            # print((self.curr_x, self.curr_y), next_coord)
            self.maze.move_pos(self.absolute_dir(next_dir))
            self.move(*next_coord)
            self.sense()


def main():

    # Each bit represents a wall 0b[WEST][SOUTH][EAST][NORTH]. Note that
    # interior wall information are stored in two cells.'''
    maze = [
        [11, 11, 9, 5, 5, 3, 11, 13, 3],
        [8, 2, 8, 7, 13, 2, 8, 7, 10],
        [14, 10, 8, 7, 9, 2, 12, 3, 10],
        [13, 4, 0, 7, 14, 10, 11, 10, 10],
        [13, 1, 6, 11, 9, 2, 8, 4, 6],
        [13, 2, 9, 2, 12, 6, 10, 9, 3],
        [9, 4, 2, 10, 11, 13, 4, 6, 10],
        [10, 9, 6, 12, 4, 1, 5, 7, 10],
        [14, 14, 13, 5, 5, 4, 5, 5, 6],
    ]

    START_X = 0
    START_Y = 8
    START_DIR = D.NORTH
    """
    x->
    (0, 0) (1, 0) (2, 0). . . 
    (0, 1) (1, 1) (2, 1). . . 
    (0, 2) (1, 2) (2, 2). . . 
    .       .
    .       .
    .       .
    """
    maze = Maze(maze, START_X, START_Y)

    solver = Solver(maze, START_X, START_Y, START_DIR)
    solver.run()


if __name__ == '__main__':
    main()
