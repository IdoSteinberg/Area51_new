from pybricks.hubs import PrimeHub
from pybricks.robotics import DriveBase
from pybricks.pupdevices import Motor
from pybricks.parameters import Port

hub = PrimeHub()
left_motor = Motor(Port.A)
right_motor = Motor(Port.B)
l_arm = Motor(Port.C)
r_arm = Motor(Port.D)
robot = DriveBase(left_motor, right_motor, wheel_diameter = 81.6, axle_track = 87)
gyro = hub.motion_sensor

def pid(speed ,desired_angle,desired_distance,kp,ki,kd):
    robot.reset()
    integral = 0
    derivative = 0
    pid_output = 0
    last_error = 0
    gyro.reset_heading()
    print(gyro.heading(), bool(desired_distance != 0), bool(desired_angle == 0))
    if desired_distance != 0:
        while abs(robot.distance()) <= desired_distance:
            error = desired_angle - gyro.heading()
            integral += error
            derivative = error - last_error
            pid_output = (error * kp) + (integral * ki) + (derivative * kd)
            last_error = error
            robot.drive(speed, pid_output)
            print(gyro.heading(), error, robot.distance())
            print(pid_output, integral, derivative, error, last_error)
    else:
        while not (desired_angle - 1) < gyro.heading() < (desired_angle + 1):
            error = desired_angle - gyro.heading()
            integral += error
            derivative = error - last_error
            pid_output = (error * kp) + (integral * ki) + (derivative * kd)
            last_error = error
            left_motor.run(pid_output*speed/200)
            right_motor.run(-(pid_output*speed/200))
            print(gyro.heading(), error)
            print(pid_output, integral, derivative, error, last_error)
    robot.stop()
    left_motor.brake
    right_motor.brake
"""
EV3 Version

#!/usr/bin/env pybricks-micropython

import time
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

ev3 = EV3Brick()
left_motor = Motor(Port.B)
right_motor = Motor(Port.D)
l_arm = Motor(Port.C)
r_arm = Motor(Port.A)
robot = DriveBase(left_motor, right_motor, wheel_diameter = 81.6, axle_track = 87) #למדוד את הרובוט ולשנות מידת 
gyro = GyroSensor(Port.S2)
integral = 0
derivative = 0
pid_output = 0
last_error = 0
print(gyro.angle())
def pid(speed ,desired_angle,desired_distance,kp,ki,kd):
    robot.reset()
    integral = 0
    derivative = 0
    pid_output = 0
    last_error = 0
    gyro.reset_angle(0)
    print(gyro.angle(), bool(desired_distance != 0), bool(desired_angle == 0))
    if desired_distance != 0:
        while abs(robot.distance()) <= desired_distance:
            error = desired_angle - gyro.angle()
            integral += error
            derivative = error - last_error
            pid_output = (error * kp) + (integral * ki) + (derivative * kd)
            last_error = error
            robot.drive(speed, pid_output)
            print(gyro.angle(), error, robot.distance())
            print(pid_output, integral, derivative, error, last_error)
    else:
        while not (desired_angle - 1) < gyro.angle() < (desired_angle + 1):
            error = desired_angle - gyro.angle()
            integral += error
            derivative = error - last_error
            pid_output = (error * kp) + (integral * ki) + (derivative * kd)
            last_error = error
            left_motor.run(pid_output*speed/200)
            right_motor.run(-(pid_output*speed/200))
            print(gyro.angle(), error)
            print(pid_output, integral, derivative, error, last_error)
    robot.stop()
    left_motor.brake
    right_motor.brake
# pid(speed ,desired_angle,desired_distance,kp,ki,kd)
#ראן
'''
ערכים אידיאליים: 
(?00, 0 - forward (? - turn), ?, 2.75, 0.001, 0.025)

'''
p = 2.75
i = 0.001
d = 0.025

pid(200, -54, 350, 2.75, 0.001, 0.025)
pid(-200, 0, 280, 2.75, 0.001, 0.025)
pid(200, 20, 0, 2.75, 0.001, 0.025)
pid(200, 0, 550, 2.75, 0.001, 0.025)
pid(-200, 0, 250, 2.75, 0.001, 0.025)
pid(200, -20, 380, 2.75, 0.001, 0.025)
l_arm.run_angle(-400, 300)
pid(-100, -5, 100, 2.75, 0.001, 0.025)
pid(-100, -34, 170, 2.75, 0.001, 0.025)
l_arm.run_angle(300, 300)
pid(200, 0, 30, 2.75, 0.001, 0.025)
pid(200, 125, 0, 2.75, 0.001, 0.025)
pid(200, 0, 200, 2.75, 0.001, 0.025)
pid(-200, 0, 130, 2.75, 0.001, 0.025)
pid(-200, -35, 300, 2.75, 0.001, 0.025)
pid(-500, -55, 500, 2.75, 0.001, 0.025)
"""