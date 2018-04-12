from ev3dev.ev3 import *
from time import *
##################################
## Skrypt do testowania koloru - zwraca wartości zczytane z czytnika(Chyba prawego ale jakby coś się psuło to warto sprawdzić).
## Można też tutaj sprawdzić czy wejście do skryptu podnoszenia działa 
##################################




def colorSum(colorSensor):
	color = colorSensor.value(0) + colorSensor.value(1) + colorSensor.value(2)
	return color	
#Stałe do wykrywania kolorów
	#Zielony
lowerGreenThreshold = 150		# Dolna granica wartości G
upperGreenThreshold = 200		# Górna granica wartości G
lowerSumGreenThreshold = 230	# Dolna granica sumy wartości
upperSumGreenThreshold = 350	# Górna granica sumy wartości
upperThetaGreenThreshold = -60	# Górna granica pomocniczej zmiennej Theta

#Sensor Initialization

	#Light
cl_right = ColorSensor('in1')
cl_left = ColorSensor('in2')

cl_right.mode='RGB-RAW'
cl_left.mode='RGB-RAW'

theta = (cl_left.value(0) - cl_left.value(1) + cl_left.value(0) - cl_left.value(2))
print("The green is " , cl_left.value(1) , " , the sum is " , colorSum(cl_left) ,"and the theta is" , theta)

if((lowerGreenThreshold < cl_left.value(1) < upperGreenThreshold ) and (lowerSumGreenThreshold<colorSum(cl_left)<upperSumGreenThreshold) and (theta < upperThetaGreenThreshold)): # or (90 < cl_right.value(1) < 160 )):# and countTheta(cl_left,cl_right) < -45):
	print("FOUND IT!")

	
