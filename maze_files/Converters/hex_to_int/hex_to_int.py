# converts correctly positions incorrect

maze=[]

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

def writeMaze(maze):
    """
    It takes a maze and writes it to a file
    
    :param maze: The maze to be written to a file
    """
    newName = name.split(".")
    newName = newName[0] + "_int." + newName[1]
    f = open(newName,"w")
    for line in maze:
        f.write("[")
        for i in line:
            f.write(str(i)+",")
        f.write("]")
        f.write(",\n")
    f.close()

def transform(maze):
    """
    It converts the hexadecimal values in the maze to integers
    
    :param maze: The maze to be transformed
    :return: The maze is being returned.
    """
    for x in range(len(maze)):
        for y in range(len(maze)):
            hex = maze[x][y]
            maze[x][y] = int(hex,16)
    return maze

def reposition(maze):
    newMaze = list(list(0 for j in range(len(maze))) for i in range(len(maze)))
    col = 0
    for line in maze:
        for i in range(len(line)):
            newMaze[15-i][col] = line[i]
        col+=1
    return newMaze
    
# 0,0 is top left
mazes = ["TAIWAN2015-FINALS.txt","Japan2013ef.txt","UK2016-final.txt","apec2018.txt","boston.txt","japan2017ef.txt",
"killer.txt","robotic-2011-solver-finals.txt","expo93.txt","uk-techfets-2017-final.txt","nagoya2002.txt"] # list of names of mazes files to be converte
for name in mazes:
    maze = getMaze(name)
    maze = transform(maze)
    maze = reposition(maze)
    writeMaze(maze)