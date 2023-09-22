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
    print("Error : %.2f  Cum Error : %.2f  Rate Error : %.2f" %
          (error, cumError, rateError))

    change = p * error + i * cumError + d * rateError
    if change > max_change:
        change = max_change
    elif change < -1 * max_change:
        change = -1 * max_change

    leftSpeed = base_speed + change
    rightSpeed = base_speed - change

    return leftSpeed, rightSpeed
