
from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Port
from umath import pi

class Drivebase:

    def __init__(self):
        hub = PrimeHub()
        self.leftMotor = Motor(Port.A)
        self.rightMotor = Motor(Port.B)
        self.l_arm = Motor(Port.C)
        self.r_arm = Motor(Port.D)
        self.gyro = hub.imu
        self.WHEEL_DIAMETER = 8.16
        self.WHEEL_CIRCUMFERENCE = self.WHEEL_DIAMETER * pi
        self.WHEEL_BASE = 12.0
    
    def drivePID(self, speed1, pid_output1):
        left_speed  = speed1 - pid_output1
        right_speed = speed1 + pid_output1
        self.leftMotor.run(left_speed * 360 / (pi * self.WHEEL_DIAMETER))
        self.rightMotor.run(right_speed * 360 / (pi * self.WHEEL_DIAMETER))
    
    def TurnPID(self, speed2, pid_output2):
        speed = speed2*pid_output2/200
        self.leftMotor.run(speed * 360 / (pi * self.WHEEL_DIAMETER))
        self.rightMotor.run(-speed * 360 / (pi * self.WHEEL_DIAMETER))

    def run_tank(self, valLeft, valRight):
        self.rightMotor.run(valRight)
        self.leftMotor.run(valLeft)

    def getDistance(self):
        return (self.rightMotor.angle() + self.leftMotor.angle()) / 2 / 360 * self.WHEEL_CIRCUMFERENCE

    def resetDistance(self):
        self.leftMotor.reset_angle(0)
        self.rightMotor.reset_angle(0)

    def resetMotors(self, leftAngle, rightAngle):
        self.leftMotor.reset_angle(leftAngle)
        self.rightMotor.reset_angle(rightAngle)

    def getGyro(self):
        return self.gyro.heading()

    def resetGyro(self):
        self.gyro.reset_heading()
    
    def GetLeftAngle(self):
        return self.leftMotor.angle()
    
    def GetRightAngle(self):
        return self.rightMotor.angle()

    def stop(self):
        self.leftMotor.brake
        self.rightMotor.brake
    
    def test_motors(self):
        self.l_arm.run(300)
        self.l_arm.run(-300)
        self.r_arm.run(300)
        self.r_arm.run(-300)