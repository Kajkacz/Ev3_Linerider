
from ev3dev.ev3 import *
from time import *
##################################
## Skrypt który nie realizuje transportu a tylko jedzie po lini
##################################

def colorSum(colorSensor):
	color = colorSensor.value(0) + colorSensor.value(1) + colorSensor.value(2)
	return color	

#Steering module alt. 2: "less aggressive". A less aggressive algorithm that adjusts the power on each motor from 0-100% (never reverse)
def steering(course, power):
	if ( colorSum(cl_right) + colorSum(cl_left) <150): #Checking for crosroads
		power_right=power_left=power
	else:
		if colorSum(cl_right) < colorSum(cl_left): #if course >= 0: 
			if course > 100:
				power_right = 0
				power_left = power
			else:	
				power_left = power
				power_right = power - ((power * course) / 100)
		else:
			
			if  course > 100: #course < -100:
				power_left = 0
				power_right = power
			else:
				power_right = power
				power_left = power + ((power * course) / 100)
	return (int(power_left), int(power_right))


def run(power, target, kp, kd, ki, minRef, maxRef): #Wersja "Poprawiona" 
	lastError = error = integral = 0
	left_motor.run_forever(speed_sp = power)
	right_motor.run_forever(speed_sp = power) 
	
	while(True): #not btn.any() :
		#print(ifs.value())
		if ts.value():
			print ('Breaking loop') # User pressed touch sensor
			break
		refRead = (colorSum(cl_right) + colorSum(cl_left))/2
		error = target - (100 * ( refRead - minRef ) / ( maxRef - minRef ))
		derivative = error - lastError
		lastError = error
		integral = float(0.5) * integral + error
		course = kp * error + kd * derivative +ki * integral
		power_left, power_right = steering(course, power)
		left_motor.run_forever(speed_sp = power_left)
		right_motor.run_forever(speed_sp = power_right)	
		sleep(0.01)

#Engine Initialization

mB = MediumMotor('outB')
left_motor = LargeMotor('outC');  #assert left_motor.connected
right_motor = LargeMotor('outD'); #assert right_motor.connected

stopSpeed = 0
pickedUp = False

#Sensor Initialization

	#Light
cl_right = ColorSensor('in1')
cl_left = ColorSensor('in2')

cl_right.mode='RGB-RAW'
cl_left.mode='RGB-RAW'

	#Proximity
ifs = InfraredSensor('in3')
	
ifs.mode = 'IR-PROX'
	#Touch
ts = TouchSensor('in4')

#btn = Button()

#VALUES

power = 250
#lub przypisać na stałe
minRef = 92
maxRef = 800

#bialy
target = 700
kp = float(0.65)
kd = 1
ki = float(0.02)
turningSpeed = 100
left_green = False
green = False

run(power, target, kp, kd, ki, minRef, maxRef)

print ('Stopping motors')
left_motor.run_forever(speed_sp = stopSpeed)
right_motor.run_forever(speed_sp = stopSpeed)
