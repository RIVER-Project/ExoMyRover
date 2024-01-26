#Pulse width range global parameters
servo180_1 = 535
servo180_2 = 2590

#Speed global parameters
stopSpeed = 0.03
maxSpeed = 1


#Angle global parameters
maxAngle = 180
minAngle = 0
neutralAngle = 90


#Direction global parameters
forwardDirection = 1
backwardDirection = -1
noDirection = 0

#Import necessary libraries
from typing import Any
from adafruit_servokit import ServoKit


#Create the kit object of the ServoKit class from the Adafruit library
kit = ServoKit(channels=16)


#Set PWM range for each 180 motor
for i in range(6, 12):
    kit.servo[i].set_pulse_width_range(servo180_1, servo180_2)


#Create the Joint class. It will be used to control each 2 motors(one 180 and one 360) of any of the 6 joints of the rover
class Joint:

    #Constructor
    def __init__(self, id360, id180, angle=None, speed=None, direction=None):

        if id360<0 or id360>5:
            raise Exception("id360 must be between 0-5")
        else:
         self._id360 = id360        #private argument

        if id180<6 or id180>11:
            raise Exception("id180 must be between 6-11")
        else:
         self._id180 = id180        #private argument

        if angle is None:
            angle = []
        elif angle<minAngle or angle>maxAngle:
            raise Exception("Angle must be between 0-180")
        self.angle = neutralAngle             #public argument, default is neutralAngle(globally defined as 90)

        if speed is None:
            speed = []
        elif speed<stopSpeed or speed>maxSpeed:
          raise Exception("Speed must be between 0.03 and 1")
        self.speed = stopSpeed      #public argument, default is stopSpeed (globally defined as 0.03)

        if direction is None:
            direction = []
        elif direction!=backwardDirection and direction!=forwardDirection and direction!=noDirection:
          raise Exception("Direction must be 0, -1 or 1")
        self.direction = noDirection          #public argument, default is noDirection (globally defined as 0)


    #Function for printing the objects
    def __str__(self):
        return f"{self.angle}, {self.speed}, {self.direction}"
    
    
    #Move function, with angle, speed and direction as parameters
    def Move(self, angle, speed, direction):
       
       if angle<minAngle or angle>maxAngle:
          raise Exception("Angle must be between 0-180")
       else:
        self.angle = angle

       if speed<stopSpeed or speed>maxSpeed:
          raise Exception("Speed must be between 0.03 and 1")
       else:
        self.speed = speed
       
       if direction!=backwardDirection and direction!=forwardDirection and direction!=noDirection:
          raise Exception("Direction must be 0, -1 or 1")
       elif self._id360 in [0, 2, 4]:  #correction for the left-side 360 motors
          direction = direction * (-1)
       else:
        self.direction = direction

       kit.servo[self._id180].angle = angle

       if speed == stopSpeed:
        kit.continuous_servo[self._id360].throttle = stopSpeed
       else:
        kit.continuous_servo[self._id360].throttle = speed * direction


    #Stop function sets the throttle speed to stopSpeed(globally declared as 0.03)
    def Stop(self):
        kit.continuous_servo[self._id360].throttle = stopSpeed

class Rover:
   def __init__(self, FLJ_obj, FRJ_obj, MLJ_obj, MRJ_obj, RLJ_obj, RRJ_obj):
      self.FLJ_obj = FLJ_obj
      self.FRJ_obj = FRJ_obj
      self.MLJ_obj = MLJ_obj
      self.MRJ_obj = MRJ_obj
      self.RLJ_obj = RLJ_obj
      self.RRJ_obj = RRJ_obj

   def Move_forward(self, angle):
      self.FLJ_obj.Move(int(angle), maxSpeed, forwardDirection)
      self.FRJ_obj.Move(int(angle), maxSpeed, forwardDirection)
      self.MLJ_obj.Move(neutralAngle, maxSpeed, forwardDirection)
      self.MRJ_obj.Move(neutralAngle, maxSpeed, forwardDirection)
      self.RLJ_obj.Move(neutralAngle, maxSpeed, forwardDirection)
      self.RRJ_obj.Move(neutralAngle, maxSpeed, forwardDirection)
   def Move_backward(self, angle):
      self.FLJ_obj.Move(neutralAngle, maxSpeed, backwardDirection)
      self.FRJ_obj.Move(neutralAngle, maxSpeed, backwardDirection)
      self.MLJ_obj.Move(neutralAngle, maxSpeed, backwardDirection)
      self.MRJ_obj.Move(neutralAngle, maxSpeed, backwardDirection)
      self.RLJ_obj.Move(int(180-angle), maxSpeed, backwardDirection)
      self.RRJ_obj.Move(int(180-angle), maxSpeed, backwardDirection)
   def Stop_rover(self):
      self.FLJ_obj.Move(neutralAngle, stopSpeed, noDirection)
      self.FRJ_obj.Move(neutralAngle, stopSpeed, noDirection)
      self.MLJ_obj.Move(neutralAngle, stopSpeed, noDirection)
      self.MRJ_obj.Move(neutralAngle, stopSpeed, noDirection)
      self.RLJ_obj.Move(neutralAngle, stopSpeed, noDirection)
      self.RRJ_obj.Move(neutralAngle, stopSpeed, noDirection)
   def Crab_walk(self, direction):
      self.FLJ_obj.Move(maxAngle, maxSpeed, direction)
      self.FRJ_obj.Move(maxAngle, maxSpeed, direction)
      self.MLJ_obj.Move(maxAngle, maxSpeed, direction)
      self.MRJ_obj.Move(maxAngle, maxSpeed, direction)
      self.RLJ_obj.Move(maxAngle, maxSpeed, direction)
      self.RRJ_obj.Move(maxAngle, maxSpeed, direction)


#Create the main function
def main():
 
 #Create the 6 objects using the corresponding id for each motor (see list below)       
       
 ###360
 #front_left360 = 0
 #front_right360 = 1
 #middle_left360 = 2
 #middle_right360 = 3
 #rear_left360 = 4
 #rear_right360 = 5
        
 ###180
 #front_left180 = 6
 #front_right180 = 7
 #middle_left180 = 8
 #middle_right180 = 9
 #rear_left180 = 10
 #rear_right180 = 11
        
 FLJ = Joint(0, 6)  #Front Left Joint
 FRJ = Joint(1, 7)  #Front Right Joint
 MLJ = Joint(2, 8)  #Middle Left Joint
 MRJ = Joint(3, 9)  #Middle Right Joint
 RLJ = Joint(4, 10) #Rear Left Joint
 RRJ = Joint(5, 11) #Rear Right Joint


 #Create the Rover object, having as arguments the 6 Joint objects
 Rover_obj = Rover(FLJ, FRJ, MLJ, MRJ, RLJ, RRJ)


 while True:
    try:
       choice = int(input("\nOptions:\n1. Move forward\n2. Move backward\n3. Crab walk\n4. Stop\n"))
       if choice == 1:
        angle = int(input('\nANGLE (0-180): \n'))
        Rover_obj.Move_forward(angle)
       elif choice == 2:
        angle = int(input('\nANGLE (0-180): \n'))
        Rover_obj.Move_backward(angle)
       elif choice == 3:
          direction = int(input('\nDIRECTION (left = -1 or right = 1): \n'))
          Rover_obj.Crab_walk(direction)
       elif choice == 4:
        Rover_obj.Stop_rover()
       else:
          print("Exiting the program")
    except ValueError:
     print("Invalid input. Please enter an integer.")          


if __name__ == "__main__":
    main()
