from pybricks.tools import wait
from controllers.Odometry import odometry
from controllers.DriveBase import Drivebase
from controllers.PID_as_class import PID

class WAYPOINT:
    """Class to manage waypoint navigation using odometry and pure pursuit control.
    
    Attributes:
        odometry: Odometry object to track robot position and orientation.
        motors: MotorManagerBig object to control the robot's motors.
        gyro: GYRO_SENSOR object to read gyroscopic data.
        pps: Pure_Pursuit_Controller object to compute control signals.
    """
    def __init__(self, odometry, motors, gyro, pps,SpiritContoller):
        # Initialize odometry for position tracking
        self.odometry = odometry
        # Initialize motors for robot movement
        self.motors = motors
        # Initialize gyro for orientation data
        self.gyro = gyro
        # Initialize pure pursuit controller for path following
        self.pps = pps

        self.SpiritContoller = SpiritContoller

    def controller_PPC(self, velocity, initial_pose=(0.0, 0.0, 0.0)):
        """Executes pure pursuit control to follow a path.
        
        Args:
            velocity: Desired speed of the robot.
            initial_pose: Tuple of (x, y, theta) for initial position and orientation.
        """
        # Reset odometry to the initial pose
        self.odometry.reset(*initial_pose)

        self.odometry.update()
            # Get current x-coordinate
        currentX = self.odometry.get_x()
            # Get current y-coordinate
        currentY = self.odometry.get_y()
            # Get current orientation (theta)
        currentTheta = self.odometry.get_theta()


        # Continue until path is complete or max ticks reached
        while not(self.pps.finish(currentX,currentY)) :
            # Update odometry to get current position
            self.odometry.update()

            # Get current x-coordinate
            currentX = self.odometry.get_x()
            # Get current y-coordinate
            currentY = self.odometry.get_y()
            # Get current orientation (theta)
            currentTheta = self.odometry.get_theta()

            # Compute angular velocity using pure pursuit controller
            w = self.pps.controller(currentX, currentY, currentTheta)

            # Calculate left motor speed
            left_speed = int(velocity - w)
            # Calculate right motor speed (negative for differential drive)
            right_speed = int(velocity + w)

            # Print current state for debugging
            print('x:', currentX, 'y:', currentY, 'theta:', currentTheta, 'left:', left_speed, 'right:', right_speed)
            # Run motors in tank mode (left and right speeds)
            self.motors.RUN_TANK(left_speed, -right_speed)
            # Wait 10ms to control loop frequency
            wait(10)


        # Stop motors when done
        self.motors.STOP()

    def SpiritController(self, velocity, initial_pose=(0.0, 0.0, 0.0), axelTrack):
        """Executes pure pursuit control to follow a path.
        
        Args:
            velocity: Desired speed of the robot.
            initial_pose: Tuple of (x, y, theta) for initial position and orientation.
        """
        # Reset odometry to the initial pose
        self.odometry.reset(*initial_pose)

        self.odometry.update()
            # Get current x-coordinate
        currentX = self.odometry.get_x()
            # Get current y-coordinate
        currentY = self.odometry.get_y()
            # Get current orientation (theta)
        currentTheta = self.odometry.get_theta()


        # Continue until path is complete or max ticks reached
        while not(self.SpiritContoller.finish(currentX,currentY)) :
            # Update odometry to get current position
            self.odometry.update()

            # Get current x-coordinate
            currentX = self.odometry.get_x()
            # Get current y-coordinate
            currentY = self.odometry.get_y()
            # Get current orientation (theta)
            currentTheta = self.odometry.get_theta()

            # Compute angular velocity using pure pursuit controller
            v,w = self.SpiritContoller.compute(currentX, currentY, currentTheta)

            left = v - w * (axle_track / 2)

            right = v + w * (axle_track / 2)

            # Print current state for debugging
            print('x:', currentX, 'y:', currentY, 'theta:', currentTheta, 'left:', left_speed, 'right:', right_speed)
            # Run motors in tank mode (left and right speeds)
            self.motors.RUN_TANK(left, -right)
            # Wait 10ms to control loop frequency
            wait(10)
