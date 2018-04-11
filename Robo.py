from ev3dev.ev3 import *
from time   import sleep

def colorWhite(colorSensor):
	white = False
	red = colorSensor.value(0)
	green = colorSensor.value(1)
	blue = colorSensor.value(2)
	if (red + green + blue) > 400:
		white = True
	#print("red ",red," green ",green," blue ",blue)
	forwardSpeed = (red+green+blue)/3
	return white


#Sensor Initialization
	#Light
cl1 = ColorSensor('in1')
cl2 = ColorSensor('in2')

cl1.mode='RGB-RAW'
cl2.mode='RGB-RAW'

#Engine Initialization

mB = MediumMotor('outB')
mC = LargeMotor('outC')
mD = LargeMotor('outD')

endPickup=True
normalSpeed = 250 
forwardSpeed = 250
turningSpeed = 100
stopSpeed = 0
turningTime = 1
pickedUp = False

	#Proximity
ifs = InfraredSensor('in3')
	
ifs.mode = 'IR-PROX'
	#Touch
ts = TouchSensor('in4')



#Main loop of program
while(True):
	sumLeft = cl1.value(0) + cl1.value(1) + cl1.value(2) 
	sumRight = cl2.value(0) + cl2.value(1) + cl2.value(2)
	theta = (cl1.value(0) - cl1.value(1) + cl1.value(0) - cl1.value(2))
	#print("Theta is " ,theta)
	
	if( 180 < sumLeft < 240 and 90 < cl1.value(1) < 150 and theta < -45 and endPickup):
		print("IM IN !!!!! COLOR 1", cl1.value(0),  cl1.value(1), cl1.value(2))
		print("COLOR 2", cl2.value(0),  cl2.value(1), cl2.value(2))
		while(endPickup):
			if(ifs.value()>25 and not pickedUp):
				mC.run_forever(speed_sp = turningSpeed)
				mD.run_forever(speed_sp = -turningSpeed)
			#print(ifs.value())
			if(ifs.value()<20 and not pickedUp):
				mC.run_forever(speed_sp = turningSpeed)
				mD.run_forever(speed_sp = turningSpeed)
			if(ifs.value()<2 and not pickedUp):
				mC.run_forever(speed_sp = 0)
				mD.run_forever(speed_sp = 0)
				mB.run_forever(speed_sp = -50)
				sleep(3)
				mB.run_forever(speed_sp = 0)
				pickedUp=True
				while (theta < -20 or theta > 5):
					theta = (cl1.value(0) - cl1.value(1) + cl1.value(0) - cl1.value(2))
					mC.run_forever(speed_sp = -turningSpeed)
					mD.run_forever(speed_sp = -turningSpeed)
					print("Theta is " ,theta)

				mC.run_forever(speed_sp = 0)
				mD.run_forever(speed_sp = 0)
			
	#Jazda przez skrzyżowania/po lini wprost
	if ((colorWhite(cl1) == True) and (colorWhite(cl2) == True) or (colorWhite(cl1) == False) and (colorWhite(cl2) == False)):
		#mB.run_forever(speed_sp = turningSpeed)
		forwardSpeed = ((sumLeft + sumRight)/150)**2
		mC.run_forever(speed_sp = forwardSpeed)
		mD.run_forever(speed_sp = forwardSpeed)
		#print(ifs.value())
		#print(forwardSpeed)

	#Korekcja w prawo na lini
	if (colorWhite(cl1) == True) and (colorWhite(cl2) == False):
		mC.run_forever(speed_sp = -forwardSpeed/3)
		mD.run_forever(speed_sp = forwardSpeed/3)
	#Korekcja w lewo na lini	
	if (colorWhite(cl1) == False) and (colorWhite(cl2) == True):
		mD.run_forever(speed_sp = -forwardSpeed/3)
		mC.run_forever(speed_sp = forwardSpeed/3)	
	#print("COLOR 1", cl1.value(0),  cl1.value(1), cl1.value(2))

#print("val1 %d val2 %d ", cl1.value(), cl2.value())
	
mC.run_forever(speed_sp = stopSpeed)
mD.run_forever(speed_sp = stopSpeed)


#getColorToConsole(cl1,"1")
#getColorToConsole(cl2,"2")



