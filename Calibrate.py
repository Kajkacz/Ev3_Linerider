from ev3dev.ev3 import *
from time import *
##################################
##Pokazuje wartości czerwonego, zielonego, sumy i thety dla obecnego miejsca w którym stoi robot
##################################

def colorSum(colorSensor):
	color = colorSensor.value(0) + colorSensor.value(1) + colorSensor.value(2)
	return color	
	
#Engine Initialization

mB = MediumMotor('outB')
left_motor = LargeMotor('outC');  #assert left_motor.connected
right_motor = LargeMotor('outD'); #assert right_motor.connected

stopSpeed = 0
pickedUp = False

#Sensor Initialization

	#Light
cl_right = ColorSensor('in2')
cl_left = ColorSensor('in1')

cl_right.mode='RGB-RAW'
cl_left.mode='RGB-RAW'

	#Proximity
ifs = InfraredSensor('in3')
	
ifs.mode = 'IR-PROX'
	#Touch
ts = TouchSensor('in4')

#btn = Button()

#VALUES

power = 150
#lub przypisać na stałe
minRef = 92
maxRef = 800

#bialy
target = 700
kp = float(0.65)
kd = 1
ki = float(0.02)

#left_motor.run_direct(duty_cycle_sp=30)
#right_motor.run_direct(duty_cycle_sp=30)
max_ref = -1000
min_ref = 1000
end_time = time() + 5

print('Values for red')
while time() < end_time:
  read = cl_right.value(0)
  if max_ref < read:
    max_ref = read
  if min_ref > read:
    min_ref = read
   
print ('Max Red: ' + str(max_ref))
print ('Min Red: ' + str(min_ref))
 
max_ref = -1000 #reset
min_ref = 1000
end_time = time() + 5

print('Values for green')
while time() < end_time:
  read = cl_right.value(1)
  if max_ref < read:
    max_ref = read
  if min_ref > read:
    min_ref = read
   
print ('Max Green: ' + str(max_ref))
print ('Min Green: ' + str(min_ref))
 
max_ref = -1000 #reset
min_ref = 1000
end_time = time() + 5

print('Values for  color sum')
while time() < end_time:
  read = colorSum(cl_right)
  if max_ref < read:
    max_ref = read
  if min_ref > read:
    min_ref = read
   
print ('Max Color Sum: ' + str(max_ref))
print ('Min Color Sum: ' + str(min_ref))

max_ref = -1000
min_ref = 1000
end_time = time() + 5

print('Values of Theta')
while time() < end_time:
  read = cl_right.value(0) - cl_right.value(1) + cl_right.value(0) - cl_right.value(2)
  if max_ref < read:
    max_ref = read
  if min_ref > read:
    min_ref = read
print ('Max Theta : ' + str(max_ref))
print ('Min Theta : ' + str(min_ref))

left_motor.stop()
right_motor.stop()

sleep(1)
