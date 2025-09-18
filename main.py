
from controllers.DriveBase import Drivebase
from controllers.PID_as_class import PID

robot = Drivebase()

pid = PID(2.75, 0.01, 0.025)

class Runs:

    def run1():
        pid.forward(999, 999, 999)
        pid.turn(999, 999, 999)
    def run2():
        pid.forward(999, 999 ,999)
        pid.turn(999, 999, 999)
    #example for now with only PID

#Runs.run1()
#Runs.run2() #example for now
print('D')