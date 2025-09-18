'''
from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Port
'''

from DriveBase import Drivebase

'''
hub = PrimeHub()
left_motor = Motor(Port.A)
right_motor = Motor(Port.B)
l_arm = Motor(Port.C)
r_arm = Motor(Port.D)
'''
robot = Drivebase()

def pid(speed ,desired_angle,desired_distance,kp,ki,kd):
    robot.reset()
    integral = 0
    derivative = 0
    pid_output = 0
    last_error = 0
    robot.resetGyro()
    if desired_distance != 0:
        while abs(robot.getDistance()) <= desired_distance:
            error = desired_angle - robot.getGyro()
            integral += error
            derivative = error - last_error
            pid_output = (error * kp) + (integral * ki) + (derivative * kd)
            last_error = error
            robot.drivePID(speed, pid_output)
    else:
        while not (desired_angle - 1) < robot.getGyro() < (desired_angle + 1):
            error = desired_angle - robot.getGyro()
            integral += error
            derivative = error - last_error
            pid_output = (error * kp) + (integral * ki) + (derivative * kd)
            last_error = error
            robot.TurnPID(speed, pid_output)
            #old version in TempPID
    robot.stop()