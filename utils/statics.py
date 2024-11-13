import math

MotorPollDelay = 0.05
USSensorPort = 2
LeftMotorPort = "A"
RightMotorPort = "D"
MotorPowerLimit = 80
MotorSpeedLimit = 270
MotorTurnSpeed = 90
WheelRadius = 0.028 #check
HalfWheelBase = 0.11 #check
DistToDeg = (180 / (math.pi * WheelRadius))
OrientToDeg = HalfWheelBase/WheelRadius

