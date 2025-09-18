from DriveBase import Drivebase

robot = Drivebase()

class PID:
    def __init__(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki 
        self.kd = kd
        self.integral = 0
        self.pid_output = 0
        self.derivative = 0
        self.last_error = 0

    def reset_values(self):
        self.integral = 0
        self.pid_output = 0
        self.derivative = 0
        self.last_error = 0
    
    def forward(self, speed, angle, distance):
        self.reset_values()
        self.speed = speed
        self.d_angle = angle
        self.d_distance = distance
        robot.resetGyro()
        while abs(robot.getDistance()) <= self.d_distance:
            error = self.d_angle - robot.getGyro()
            self.integral += error
            self.derivative = error - self.last_error
            self.pid_output = (error * self.kp) + (self.integral * self.ki) + (self.derivative * self.kd)
            self.last_error = error
            robot.drivePID(self.speed, self.pid_output)
        robot.stop()

    def turn(self, speed, angle, distance):
        self.reset_values()
        self.speed = speed
        self.d_angle = angle
        self.d_distance = distance
        while not (self.d_angle - 1) < robot.getGyro() < (self.d_angle + 1):
            error = self.d_angle - robot.getGyro()
            self.integral += error
            self.derivative = error - self.last_error
            self.pid_output = (error * self.kp) + (self.integral * self.ki) + (self.derivative * self.kd)
            self.last_error = error
            robot.TurnPID(self.speed, self.pid_output)
        robot.stop()

#example:
pid = PID(kp=2.75, ki=0.01, kd=0.025)
pid.forward(200, 30, 500)
pid.turn(500, 45, 0) #note that distance doesn't matter here