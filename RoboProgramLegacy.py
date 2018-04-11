from ev3dev.ev3 import *
from time   import sleep

def getColorR(colorSensor):
	colorSensor.mode='RGB-RAW'
	return colorSensor.value(0)
	
def getColorG(colorSensor):
	colorSensor.mode='RGB-RAW'
	return colorSensor.value(1)
	
def getColorB(colorSensor):
	colorSensor.mode='RGB-RAW'
	return colorSensor.value(2)
	

def getColorToConsole(colorSensor, sensorNumber):
	colorSensor.mode='RGB-RAW'
	red = colorSensor.value(0)
	green = colorSensor.value(1)
	blue = colorSensor.value(2)
	return

def colorWhite(colorSensor):
	white = False
	red = colorSensor.value(0)
	green = colorSensor.value(1)
	blue = colorSensor.value(2)
	if (red + green + blue) > 150:
		white = True
	#print("red ",red," green ",green," blue ",blue)
	return white

mB = MediumMotor('outB')
mC = LargeMotor('outC')
mD = LargeMotor('outD')

cl1 = ColorSensor('in1')
cl2 = ColorSensor('in2')

cl1.mode='RGB-RAW'
cl2.mode='RGB-RAW'

forwardSpeed = 50;
turningSpeed = 0;
stopSpeed = 0;

while(True):
	if ((colorWhite(cl1) == True) and (colorWhite(cl2) == True) or (colorWhite(cl1) == False) and (colorWhite(cl2) == False)):
		#mB.run_forever(speed_sp = turningSpeed)
		mC.run_forever(speed_sp = forwardSpeed)
		mD.run_forever(speed_sp = forwardSpeed)
	if (colorWhite(cl1) == True) and (colorWhite(cl2) == False):
		mB.run_forever(speed_sp = 300)
	if (colorWhite(cl1) == False) and (colorWhite(cl2) == True):
		mB.run_forever(speed_sp = -300)	
#TODO : Odróżnianie czarnego od czerwonego/zielonego

#print("val1 %d val2 %d ", cl1.value(), cl2.value())
	
mC.run_forever(speed_sp = stopSpeed)
mD.run_forever(speed_sp = stopSpeed)


#getColorToConsole(cl1,"1")
#getColorToConsole(cl2,"2")



