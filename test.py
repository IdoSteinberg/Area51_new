from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch
from pybricks.tools import hub_menu

hub = PrimeHub()

# left must turn counterclockwise to make the robot go forward.
left_motor = Motor(Port.F, Direction.COUNTERCLOCKWISE)
right_motor = Motor(Port.B, Direction.COUNTERCLOCKWISE)
#it's pretty obvious what this code does
arm_1 = Motor(Port.A)
arm_2 = Motor(Port.E)


# set the axle track to the distance between the wheels.
robot = DriveBase(left_motor, right_motor, wheel_diameter=56, axle_track=112)
robot.use_gyro(True)

i_speed = 500
i_acceleration = 300
robot.settings(straight_acceleration=i_acceleration, straight_speed=i_speed)

def move(p_distance, p_radius=None, p_wait=True, p_acceleration=None, p_speed=None):
    if p_speed is not None:
        robot.settings(straight_speed=p_speed)
    if p_acceleration is not None:
        robot.settings(straight_acceleration=p_acceleration)

    if p_radius is not None:
        robot.arc(radius=p_radius, distance=p_distance, wait=p_wait)
    else:
        robot.straight(distance=p_distance, wait=p_wait)


    #reset robot settings after movement is finished
    robot.settings(straight_acceleration=i_acceleration, straight_speed=i_speed)
    return

def move_arm(arm_number, m_speed, m_time=None, m_angle=None, m_wait=True):
    if m_time is None and m_angle is None:
        return
    elif arm_number > 2 or arm_number < 1:
        return
    elif m_time is not None and m_angle is not None:
        return
    elif m_time is not None and m_angle is None and arm_number == 1:
        arm_1.run_time(speed=m_speed, time=m_time, wait=m_wait)
    elif m_time is None and m_angle is not None and arm_number == 1:
        arm_1.run_angle(speed=m_speed, rotation_angle=m_angle, wait=m_wait)
    elif m_time is not None and m_angle is None and arm_number == 2:
        arm_2.run_time(speed=m_speed, time=m_time, wait=m_wait)
    elif m_time is None and m_angle is not None and arm_number == 2:
        arm_2.run_angle(speed=m_speed, rotation_angle=m_angle, wait=m_wait)

    return



def turn(p2_angle, p2_wait=True):
    robot.turn(angle=p2_angle, wait=p2_wait)
    return

def run1():
    move(100)
    turn(90)

def run2():
    move(500, p_radius=100)

def run3():
    move(500, p_radius=100)

def run4():
    move(500, p_radius=100)

def run5():
    move(500, p_radius=100)

def run6():
    move(500, p_radius=100)

def run7():
    move(500, p_radius=100)

def run8():
    move(500, p_radius=100)

def run9():
    move(500, p_radius=100)

def run10():
    move(500, p_radius=100)

def run11():
    move(500, p_radius=100)

def run12():
    move(500, p_radius=100)

def run13():
    move(500, p_radius=100)

def run14():
    move(500, p_radius=100)

def run15():
    move(500, p_radius=100)



#I do not care that this code is inefficient
selected = hub_menu(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15)

if selected == 1:
    run1()
elif selected == 2:
    run2()
elif selected == 3:
    run3()
elif selected == 4:
    run4()
elif selected == 5:
    run5()
elif selected == 6:
    run6()
elif selected == 7:
    run7()
elif selected == 8:
    run8()
elif selected == 9:
    run9()
elif selected == 10:
    run10()
elif selected == 11:
    run11()
elif selected == 12:
    run12()
elif selected == 13:
    run13()
elif selected == 14:
    run14()
elif selected == 15:
    run15()
print("Emanuel was here")