
from ev3dev.ev3 import *
from time import *


def colorSum(colorSensor):
	color = colorSensor.value(0) + colorSensor.value(1) + colorSensor.value(2)
	return color	

def countTheta(color_sensor1, color_sensor2): #Nieużywane (?)
	theta = (2*color_sensor1.value(0) - color_sensor1.value(1) - color_sensor1.value(2) + 2*color_sensor2.value(0) - color_sensor2.value(1) - color_sensor2.value(2))/2
	return theta
	
def checkRed():
	theta = (cl_left.value(0) - cl_left.value(1) + cl_left.value(0) - cl_left.value(2))
	print("The red is " , cl_left.value(0) , " And the sum is " , colorSum(cl_left))
	
	return False
	#DOPASOWAĆ WARTOŚCI NIŻEJ, to jest tylko kalka z zielonego!I usunąć return wyżej
	
	if((lowerRedThreshold < cl_left.value(0) < upperRedThreshold ) and (lowerSumRedThreshold<colorSum(cl_left)<upperSumRedThreshold) and (theta < upperThetaRedThreshold)): # or (90 < cl_right.value(1) < 160 )):# and countTheta(cl_left,cl_right) < -45):
		return True
	else:
		return False


def checkGreen():
	theta = (cl_left.value(0) - cl_left.value(1) + cl_left.value(0) - cl_left.value(2))
	print("The green is " , cl_left.value(1) , " And the sum is " , colorSum(cl_left))
	
	if((lowerGreenThreshold < cl_left.value(1) < upperGreenThreshold ) and (lowerSumGreenThreshold<colorSum(cl_left)<upperSumGreenThreshold) and (theta < upperThetaGreenThreshold)): # or (90 < cl_right.value(1) < 160 )):# and countTheta(cl_left,cl_right) < -45):
		return True
	else:
		return False
	
def leftGreen(): #To służy do sprawdzania strony, raczej do śmieci
	if(90 < cl_left.value(1) < 150 and countTheta(cl_left,cl_right) < -45):
		return True
	if(90 < cl_right.value(1) < 150 and countTheta(cl_left,cl_right) < -45):
		return False
	return 0

def returnToLine(): 							# Funkcja wracająca robota na linię jazdy
	left_motor.run_forever(speed_sp = -power)	# Obracamy się o 180 stopni w kierunku do lini
	right_motor.run_forever(speed_sp = power)
	sleep(2*turningTimeRightAngle) 
	
	left_motor.run_forever(speed_sp = power)	# Dojeżdżamy do środka
	right_motor.run_forever(speed_sp = power)
	sleep(forwardTimeToCentre)
	
	left_motor.run_forever(speed_sp = power)	# Obracamy się o 90 stopni w kierunku jazdy
	right_motor.run_forever(speed_sp = -power)
	sleep(turningTimeRightAngle) 
			
def pickUpNaive():									# Naiwna werjsa podnoszenia 
	left_motor.run_forever(speed_sp = power)	# Obracamy się o 90 stopni w kierunku do pola podnoszenia
	right_motor.run_forever(speed_sp = -power)
	sleep(turningTimeRightAngle) 
	
	left_motor.run_forever(speed_sp = power)	# Dojeżdżamy do środka
	right_motor.run_forever(speed_sp = power)
	sleep(forwardTimeToCentre)
	
	left_motor.run_forever(speed_sp = 0)		# Zatrzymujemy silnik
	right_motor.run_forever(speed_sp = 0)
	
	mB.run_forever(speed_sp = -70)				# Podnosimy klocek
	sleep(3)
	mB.run_forever(stop_action = "hold") #Jeśli to nie działa to cofnąć do wersji niżej
	#mB.run_forever(speed_sp = 0)
	
	returnToLine()								# Wracamy do Lini jazdy
		
def pickUp():
	left_motor.run_forever(speed_sp = power)
	right_motor.run_forever(speed_sp = -power)
	blockPickedUp = False
	
	while(not blockPickedUp):
			while(ifs.value()>23 and not blockPickedUp):
				left_motor.run_forever(speed_sp = -turningSpeed)
				right_motor.run_forever(speed_sp = turningSpeed)
			#print(ifs.value())
			left_motor.run_forever(speed_sp = turningSpeed)
			right_motor.run_forever(speed_sp = turningSpeed)
			if(ifs.value()<2 and not blockPickedUp):
				left_motor.run_forever(speed_sp = 0)
				right_motor.run_forever(speed_sp = 0)
				mB.run_forever(speed_sp = -70)
				sleep(3)
				mB.run_forever(speed_sp = 0)
				#mB.hold()
				blockPickedUp=True
				remember = colorSum(cl_right) + colorSum(cl_left)
				while(( colorSum(cl_right) + colorSum(cl_left) ) - remember < 200):
					remember = colorSum(cl_right) + colorSum(cl_left)
					print(remember)
					#print( colorSum(cl_right) + colorSum(cl_left))
					left_motor.run_forever(speed_sp = -turningSpeed)
					right_motor.run_forever(speed_sp = -turningSpeed)
				while(colorSum(cl_right)<200 or colorSum(cl_left)<200 ):
					left_motor.run_forever(speed_sp = turningSpeed)
					right_motor.run_forever(speed_sp = -turningSpeed)
				#left_motor.run_forever(speed_sp = -turningSpeed)
				#right_motor.run_forever(speed_sp = +turningSpeed)
				#sleep(0.75)
				#left_motor.run_forever(speed_sp = 0)
				#right_motor.run_forever(speed_sp = 0)
				break	
		

def dropBlock(): 
	left_motor.run_forever(speed_sp = power)	# Obracamy się o 90 stopni w kierunku do pola podnoszenia
	right_motor.run_forever(speed_sp = -power)
	sleep(turningTimeRightAngle) 
	
	left_motor.run_forever(speed_sp = power)	# Dojeżdżamy do środka
	right_motor.run_forever(speed_sp = power)
	sleep(forwardTimeToCentre)
	
	left_motor.run_forever(speed_sp = 0)		# Zatrzymujemy silnik
	right_motor.run_forever(speed_sp = 0)
	
	mB.run_forever(speed_sp = 70)				# Opuszczamy klocek
	sleep(3)
	mB.run_forever(stop_action = "hold") #Jeśli to nie działa to cofnąć do wersji niżej
	#mB.run_forever(speed_sp = 0)
	
	# Jeśli nie musimy wracać na tor to poniższy kod jest zbędny
	returnToLine()
	
	

	

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
	blockPickedUp = False # Flaga o podniesieniu klocka
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

#Stałe do obrotu i ruchu przy podnoszeniu
turningTimeRightAngle = 1 					# Trzeba zahardcode'ować żeby obracał się o kąt prosty.Nie wiem jak inaczej, w sumie chyba się nie da
forwardTimeToCentre = 1					 	# Jak wyżej, tutaj dajemy wartość taką żeby dojechał do środka czerwonego pola

#Stałe do wykrywania kolorów
	#Zielony
lowerGreenThreshold = 100		# Dolna granica wartości G
upperGreenThreshold = 180		# Górna granica wartości G
lowerSumGreenThreshold = 140	# Dolna granica sumy wartości
upperSumGreenThreshold = 300	# Górna granica sumy wartości
upperThetaGreenThreshold = -60	# Górna granica pomocniczej zmiennej Theta
	# Czerwony
lowerGreenThreshold = 0			# jw. - wypełnić wartości dla czerwonego
upperGreenThreshold = 0
lowerSumGreenThreshold = 0
upperSumGreenThreshold = 0
upperThetaGreenThreshold = 0

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
# TO wyżej to nowa wersja, niżej siedzi stara
#runCycle()
print ('Stopping motors')
left_motor.run_forever(speed_sp = stopSpeed)
right_motor.run_forever(speed_sp = stopSpeed)
