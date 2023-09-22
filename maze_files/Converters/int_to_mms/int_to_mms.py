#converts correctly positions incorrect
# draw maze with integer positional representation
# and put it in test.txt file
# this will convert it to num, for the mms sim

maze=[]
size = 6
def getMaze(name):
    """
    It takes a file name, opens the file, reads the file, and returns a list of lists
    
    :param name: The name of the file that contains the maze
    :return: A list of lists.
    """
    maze = []
    with open(name, "r") as f:
        for line in f:
            maze.append(list((line.strip().split(","))))
        for line in maze:
            line.pop()
    return maze

def printMaze(maze):
    """
    It prints the maze
    
    :param maze: The maze to be solved
    """
    for line in maze:
        print(line)

def convertToBin(maze):
    """
    It converts the maze to binary
    
    :param maze: The maze to be
    """
    for line in maze:
        for i in range(len(line)):
            line[i] = bin(int(line[i]))[2:].zfill(4)
    return maze


def writeMazeToNum(maze):
    """
    It takes a maze and writes it to a file
    
    :param maze: The maze to be written to a file
    """
    newName = name.split(".")
    newName = newName[0] + "." + "num"
    f = open(newName,"w")
    for line in maze:
        for i in line:
            f.write(str(i)+"\n")
    f.close()

def flipMaze(maze):
    """
    It takes a maze and flips it
    
    :param maze: The maze to be flipped
    :return: The maze is being returned.
    """
    for x in range(size):
        for y in range(size):
            maze[x][y] = maze[x][y][::-1]
    return maze

def spaceMaze(maze):
    """
    It takes a list of lists of strings and returns a list of lists of strings
    
    :param maze: The maze to be printed
    :return: The maze with spaces between the walls.
    """
    for x in range(size):
        for y in range(size):
            maze[x][y] = maze[x][y][0] + " " + maze[x][y][1] + " " + maze[x][y][2] + " " + maze[x][y][3]
    return maze

def addCord(maze,size):
    """
    It takes a 2D array and returns a 2D array with the same values but with the coordinates of each
    element added to the front of each element
    
    :param maze: The maze you want to add coordinates to
    :param size: The size of the maze
    :return: A list of lists of strings.
    """
    newMaze = [[]for i in range(size)] 
    for line in newMaze:
        for i in range(size):
            line.append("0")

    for x in range(size):
        for y in range(size):
            newMaze[y][size-1-x] = str(y) + " " + str(size-1-x) + " " + maze[x][y]

    return newMaze

mazes = ["test6by6.txt"] # list of names of mazes files to be converted

for name in mazes:
    maze = getMaze(name)
    printMaze(maze)
    maze=convertToBin(maze)
    printMaze(maze)
    print("  ")
    maze = flipMaze(maze)
    printMaze(maze)
    print("  ")
    maze = spaceMaze(maze)
    printMaze(maze)
    print("  ")
    maze = addCord(maze,size)
    printMaze(maze)
    writeMazeToNum(maze)
