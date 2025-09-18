from DriveBase import Drivebase
from umath import pi, cos, sin, radians

robot = Drivebase()

class odometry:
    def __init__(self):
        self.X = 0.0
        self.Y = 0.0
        self.THETA = 0.0
        self.l_motor_pos = robot.GetLeftAngle()
        self.r_motor_pos = robot.GetRightAngle()
        self.gyro = robot.getGyro()
        self.wheel_radius = robot.WHEEL_DIAMETER/2
        self.WHEEL_CIRCUMFERENCE = robot.WHEEL_CIRCUMFERENCE
        self.ticks_per_rotation = 360
        self.last_a = 0
        self.last_b = 0
        self.init()

    def init(self):
        self.last_left_angle = self.l_motor_pos
        self.last_right_angle = self.r_motor_pos

    

    def update(self):
        a = self.l_motor_pos
        b = self.r_motor_pos
        delta_a = (a - self.last_left_angle) * (self.wheel_radius * 2 * pi / self.ticks_per_rotation)
        delta_b = (b - self.last_right_angle) * (self.wheel_radius * 2 * pi / self.ticks_per_rotation)
        self.last_left_angle, self.last_right_angle = a, b
        theta_deg = self.gyro
        theta = radians(theta_deg)
        dist = (delta_a + delta_b) / 2  
        dx = dist * cos(theta)
        dy = dist * sin(theta)
        self.X += dx
        self.Y += dy
        self.THETA = theta

    def odometry_loop(self):
        self.running = True
        while self.running:
            self.update(self)
    
    def stop_odometry(self):
        self.running = False

    def get_x(self):

        return self.X

    def get_y(self):

        return self.Y

    def get_theta(self):

        return self.THETA

    def reset(self, x=0.0, y=0.0, theta=0.0):

        self.X = x

        self.Y = y

        self.THETA = theta

        self.init()
