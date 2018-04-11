from ev3dev.ev3 import *

mB = MediumMotor('outB')
mC = LargeMotor('outC')
mD = LargeMotor('outD')

mB.stop(stop_action='brake')
mC.stop(stop_action='brake')
mD.stop(stop_action='brake')

mB.run_forever(speed_sp=0)
mC.run_forever(speed_sp=0)
mD.run_forever(speed_sp=0)
