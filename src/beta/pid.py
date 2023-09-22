import math
previousError, cumError = 0, 0
base_speed = 25
max_change = 25
IGNORE_ERROR_THRESHOLD = 66

p = -0.8
i = 0.01
# i = 0.25
d = -0.05
# Works when the robot is initially centered


def pid_controller(error):
    global previousError, cumError
    # error is left distance - right distance
    if abs(previousError - error) > IGNORE_ERROR_THRESHOLD:
        error = previousError

    cumError += error
    rateError = (error - previousError)
    previousError = error
    # print("Error : %.2f  Cum Error : %.2f  Rate Error : %.2f" %
        #   (error, cumError, rateError))

    change = p * error + i * cumError + d * rateError
    if change > max_change:
        change = max_change
    elif change < -1 * max_change:
        change = -1 * max_change

    leftSpeed = base_speed + change
    rightSpeed = base_speed - change

    return leftSpeed, rightSpeed

def calculate_error(leftDistance, rightDistance, bearing, orientation):
    # bearing range (0 to 360)
    # threshold: if side Length > 66, then ignore

    # return distance to centre of mass from left and right walls
    # if 
    # default left
    # if not left use right
    error = 0
    
    distanceThreshold = 66
    sensorOffsetright = 41
    sensorOffsetleft = 41

    angle = 0
    if orientation == "N":
        if (bearing >270):
            angle = bearing-360
        else:
            angle = bearing
    elif orientation == "E":
        angle = bearing-90
    elif orientation == "S":
        angle = bearing-180
    elif orientation == "W":
        angle = bearing-270

    angle = math.radians(angle)
    if leftDistance < distanceThreshold:
        # have both walls, default to left
        error = (leftDistance+sensorOffsetleft)*math.cos(angle) - 74

    elif rightDistance < distanceThreshold:
        # no left, but have right
        error = 74 - (rightDistance+sensorOffsetright)*math.cos(angle)
    else:
        # no walls
        error = math.sin(angle) * 10

    if error < -33:
        error = -33
    elif error > 33:
        error = 33
        
    return error


#testing

# ## north
# print()
# print("NORTH")
# print("centred ")
# print("angle 0")
# print (calculate_error(33,33,0,"North"))
# print("angle +3")
# print (calculate_error(80,94,3,"North")) 
# print("angle -3")
# print (calculate_error(34,34,357,"North"))
# print("----------------------------------")
# print("off to left 3mm from centre")
# print("angle 0")
# print (calculate_error(30,36,0,"North"))
# print("angle +3")
# print (calculate_error(30,36,3,"North")) 
# print("angle -3")
# print (calculate_error(30,36,357,"North"))
# print("----------------------------------")
# print("off to right 3mm from centre")
# print("angle 0")
# print (calculate_error(36,30,0,"North"))
# print("angle +3")
# print (calculate_error(36,30,3,"North")) 
# print("angle -3")
# print (calculate_error(36,30,357,"North"))
# print("----------------------------------")

# ## east
# print()
# print("EAST")
# print("centred ")
# print("angle 0")
# print (calculate_error(33,33,90,"East"))
# print("angle +3")
# print (calculate_error(33,33,93,"East")) 
# print("angle -3")
# print (calculate_error(33,33,87,"East"))
# print("----------------------------------")
# print("off to left 3mm from centre")
# print("angle 0")
# print (calculate_error(30,36,90,"East"))
# print("angle +3")
# print (calculate_error(30,36,93,"East")) 
# print("angle -3")
# print (calculate_error(30,36,87,"East"))
# print("----------------------------------")
# print("off to right 3mm from centre")
# print("angle 0")
# print (calculate_error(36,30,90,"East"))
# print("angle +3")
# print (calculate_error(36,30,93,"East")) 
# print("angle -3")
# print (calculate_error(36,30,87,"East"))
# print("----------------------------------")

# ## south
# print()
# print("SOUTH")
# print("centred ")
# print("angle 0")
# print (calculate_error(33,33,180,"South"))
# print("angle +3")
# print (calculate_error(33,33,183,"South")) 
# print("angle -3")
# print (calculate_error(33,33,177,"South"))
# print("----------------------------------")
# print("off to left 3mm from centre")
# print("angle 0")
# print (calculate_error(30,36,180,"South"))
# print("angle +3")
# print (calculate_error(30,36,183,"South")) 
# print("angle -3")
# print (calculate_error(30,36,177,"South"))
# print("----------------------------------")
# print("off to right 3mm from centre")
# print("angle 0")
# print (calculate_error(36,30,180,"South"))
# print("angle +3")
# print (calculate_error(36,30,183,"South")) 
# print("angle -3")
# print (calculate_error(36,30,177,"South"))
# print("----------------------------------")

# ## west
# print()
# print("WEST")
# print("centred ")
# print("angle 0")
# print (calculate_error(33,33,270,"West"))
# print("angle +3")
# print (calculate_error(33,33,273,"West")) 
# print("angle -3")
# print (calculate_error(33,33,267,"West"))
# print("----------------------------------")
# print("off to left 3mm from centre")
# print("angle 0")
# print (calculate_error(30,36,270,"West"))
# print("angle +3")
# print (calculate_error(30,36,273,"West")) 
# print("angle -3")
# print (calculate_error(30,36,267,"West"))
# print("----------------------------------")
# print("off to right 3mm from centre")
# print("angle 0")
# print (calculate_error(36,30,270,"West"))
# print("angle +3")
# print (calculate_error(36,30,273,"West")) 
# print("angle -3")
# print (calculate_error(36,30,267,"West"))
# print("----------------------------------")