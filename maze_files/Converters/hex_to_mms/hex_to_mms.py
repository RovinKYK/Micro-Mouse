#directly converting hex maze to mms maze
# tested and works properly

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

def writeMazeToNum(maze,name):
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

def convertToMMS(maze):
    for x in range(len(maze)):
        for y in range(len(maze)):
            temp = maze[x][y][::-1]
            temp2=""
            for i in temp:
                temp2+=i+" "
            temp = str(x)+" "+str(y)+" "+temp2
            maze[x][y] = temp[:-1]
    return maze

def convertToBin(maze):
    """
    It converts the maze to binary
    
    :param maze: The maze to be
    """
    for line in maze:
        for i in range(len(line)):
            temp = int(line[i],16)
            line[i] = bin(temp)[2:].zfill(4)
    return maze

mazes = ["TAIWAN2015-FINALS.txt","Japan2013ef.txt","UK2016-final.txt","apec2018.txt","boston.txt","japan2017ef.txt",
"killer.txt","robotic-2011-solver-finals.txt","expo93.txt","uk-techfets-2017-final.txt","nagoya2002.txt"] # list of names of mazes files to be converted
for name in mazes:
    maze = getMaze(name)
    printMaze(maze)   
    maze = convertToBin(maze)
    printMaze(maze)
    maze = convertToMMS(maze)
    printMaze(maze)
    writeMazeToNum(maze,name)