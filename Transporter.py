from ev3dev.ev3 import *
from time import *
##################################
## Skrypt realizujący zadanie transportu klocka
##################################

#Stałe do obrotu i ruchu przy podnoszeniu
turningTimeRightAngle = 0.8				# Trzeba zahardcode'ować żeby obracał się o kąt prosty.Nie wiem jak inaczej, w sumie chyba się nie da
forwardTimeToCentre = 1					# Jak wyżej, tutaj dajemy wartość taką żeby dojechał do środka czerwonego pola

power = turningSpeed = 180 				# Stała określająca prędkość jazdy i skrętu

# Wartości odniesienia dla układu PID

minRef = 92
maxRef = 800

#bialy
target = 700
kp = float(0.65)
kd = 1
ki = float(0.02)


def colorSum(colorSensor):						#Funkcja licząca sumę kolorów w danym miejscu dla podanego sensora
	color = colorSensor.value(0) + colorSensor.value(1) + colorSensor.value(2)
	return color	
	
def checkRed(colorSensor):						# Funkcja sprawdzająca czy obecny odczyt wpada w zakres czerwonego
												
	lowerThetaRedThreshold = 250				# Jako że nasza Theta jest liczona dla podwójnej wartości czerwonego to po testach zacząłem używać
												# tylko tej wartości do sprawdzania czy jestem na polu czerwonym
	theta = (colorSensor.value(0) - colorSensor.value(1) + colorSensor.value(0) - colorSensor.value(2))
	#print("The red is " , cl_left.value(0) , " and the sum is " , colorSum(cl_left), "and the Theta is " , theta)
	
	if(theta > lowerThetaRedThreshold): 		
		#print("I am in, the red is " , cl_left.value(0) , " and the sum is " , colorSum(cl_left), "and the Theta is " , theta)
		return True
	else:
		return False


def checkGreen():								# Funkcja sprawdzająca czy obecny odczyt wpada w zakres czerwonego
		#Zielony
	lowerThetaGreenThreshold = 280	# Dolna granica pomocniczej zmiennej Theta - jako że dla czerwonego działało to bardzo dobrze zmieniam warunek
									# tak aby sprawdzał wg. zmienionej wersji theta, czyli 2*G - R - B. Myślę że może to dobrze zadziałać
	theta = (2*cl_left.value(1) - cl_left.value(0) - cl_left.value(2))
	#print("The red is " , cl_left.value(0) , " and the sum is " , colorSum(cl_left), "and the Theta is " , theta)
	if(theta < upperThetaGreenThreshold):
		#print("I am in, the green is " , cl_left.value(1) , " , the sum is " , colorSum(cl_left) ,"and the theta is" , theta)	#Print readings
		return True
	else:
		return False
		
def returnToLine(): 							# Funkcja wracająca robota na linię jazdy
	global forwardTimeToCentre
	global turningTimeRightAngle
	
	left_motor.run_forever(speed_sp = -power)	# Dojeżdżamy do środka
	right_motor.run_forever(speed_sp = -power)
	sleep(forwardTimeToCentre)
	#print(forwardTimeToCentre)
	
	left_motor.run_forever(speed_sp = power)	# Obracamy się o 90 stopni w kierunku jazdy
	right_motor.run_forever(speed_sp = -power)
	sleep(turningTimeRightAngle) 

def newReturnToLine():
		# Wartości pomocnicze aby sprawdzić czy wracamy z pola zielonego czy czerwonego
	thetaRed = ( 2*colorSensor.value(0) - colorSensor.value(1)  - colorSensor.value(2))
	thetaGreen = ( 2*colorSensor.value(1) - colorSensor.value(0) - colorSensor.value(2))
	diff = 200 # Pomocniczy parametr - oznacza różnicę pomiędzy thetami jaka musi wystąpić żeby uznać że dojechaliśmy do czarnego
	sumThreshold = 200 # Jaka musi być suma aby uznać że jest czarna
	isRed = isGreen = False
	
	if(thetaRed > thetaGreen):
		isRed = True
	else:
		isGreen = True
		
	previousSum = colorSum(cl_right) + colorSum(cl_left)
	
	while(( colorSum(cl_right) + colorSum(cl_left) ) - previousSum < sumThreshold or abs(thetaRed - thetaGreen) > diff): # Wracamy do lini dla dużego skoku wartości
		previousSum = colorSum(cl_right) + colorSum(cl_left)
		thetaRed = ( 2*colorSensor.value(0) - colorSensor.value(1)  - colorSensor.value(2))
		thetaGreen = ( 2*colorSensor.value(1) - colorSensor.value(0) - colorSensor.value(2))
		
		#print("Previous sum is " , previousSum , " the theta for red is " , thetaRed , " and the theta for green is " , thetaGreen)

		left_motor.run_forever(speed_sp = -turningSpeed)
		right_motor.run_forever(speed_sp = -turningSpeed)
		
	while(colorSum(cl_right)<sumThreshold or colorSum(cl_left)<sumThreshold ):			# Obracamy robota w kierunku jazdy
		left_motor.run_forever(speed_sp = turningSpeed)
		right_motor.run_forever(speed_sp = -turningSpeed)

def pickUp():									# Funkcja podnosząca klocek
	#sleep(1)
	left_motor.run_forever(speed_sp = power)	# Robot zaczyna się obracać
	right_motor.run_forever(speed_sp = -power)
	
	blockPickedUp = False						# Flaga oznaczająca podniesienie klocka
	while(not blockPickedUp):
			distanceToBlock = 35				# Pomocnicza zmienna, oznacza dystans poniżej którego mamy przerwać obracanie i zacząć jechać w kierunku klocka
			while(ifs.value()>distanceToBlock and not blockPickedUp):
				#print(ifs.value())
				left_motor.run_forever(speed_sp = -turningSpeed) # Robot obraca się do zauważenia klocka
				right_motor.run_forever(speed_sp = turningSpeed)
			#print(ifs.value())
			left_motor.run_forever(speed_sp = turningSpeed)		 # Po zauważeniu klocka robot podjeżdża do niego
			right_motor.run_forever(speed_sp = turningSpeed)
			arrivedAtBlock = 2
			if(ifs.value() < arrivedAtBlock and not blockPickedUp): # Kiedy zbliżymy się na odległość zdefiniowaną powyżej (czyli de facto dotkniemy klocka) podnosimy widełki
				left_motor.run_forever(speed_sp = 0)		# Stop
				right_motor.run_forever(speed_sp = 0)
				
				mB.run_forever(speed_sp = -70)				# Podnieś
				sleep(3)
				mB.run_forever(stop_action = "hold")		# Jeśli to nie działa to cofnąć do wersji niżej - trzymanie klocka w górze
				#mB.run_forever(speed_sp = 0)
					
				blockPickedUp=True							# Zapamiętujemy podniesienie klocka
				
				#returnToLine() #Stare i pewne
				newReturnToLine()							# Wracamy do lini
				
				break	
		

def dropBlock(): 								# Funkcja upuszczająca klocek
	global turningTimeRightAngle
	global forwardTimeToCentre
	#print("Times : ", turningTimeRightAngle , forwardTimeToCentre)
	
	left_motor.run_forever(speed_sp = -power)	# Obracamy się o 90 stopni w kierunku do pola podnoszenia
	right_motor.run_forever(speed_sp = power)
	sleep(turningTimeRightAngle) 
	
	left_motor.run_forever(speed_sp = power)	# Dojeżdżamy do środka
	right_motor.run_forever(speed_sp = power)
	
	while(not (checkRed(cl_left)  and checkRed(cl_right))):	# Wykrywamy środek kiedy dwa sensory widzą czerwony
		print("Looking for red")
	left_motor.run_forever(speed_sp = 0)		# Zatrzymujemy silnik
	right_motor.run_forever(speed_sp = 0)
	
	mB.run_forever(speed_sp = 70)				# Opuszczamy klocek
	sleep(2)
	mB.run_forever(stop_action = "hold")		# Jeśli to nie działa to cofnąć do wersji niżej - trzymanie klocka w górze
	#mB.run_forever(speed_sp = 0)
	
	# Jeśli nie musimy wracać na tor to poniższy kod jest zbędny
	#returnToLine() #Stare i pewne
	newReturnToLine()

	

	

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
		if (checkGreen()  and not blockPickedUp):
			pickUp() 
			blockPickedUp = True
		if(checkRed(cl_left)  and blockPickedUp):
			left_motor.run_forever(speed_sp = 0)
			right_motor.run_forever(speed_sp = 0) 
			dropBlock()
			blockPickedUp = False # Niby nie potrzebne, ale po co ryzykować
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

run(power, target, kp, kd, ki, minRef, maxRef) # Główna funkcja kontrolująca jazdę

print ('Stopping motors')
left_motor.run_forever(speed_sp = stopSpeed)
right_motor.run_forever(speed_sp = stopSpeed)
