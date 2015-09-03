import sys,os,ctypes,time
import api

def rightSideForwards():
	api.SetMotorValue(4,612)
	api.SetMotorValue(12,500)

def rightSideBackwards():
	api.SetMotorValue(4,524)
	api.SetMotorValue(12,412)

def leftSideForwards():
	api.SetMotorValue(3,412)
	api.SetMotorValue(11,524)

def leftSideBackwards():
	api.SetMotorValue(3,500)
	api.SetMotorValue(11,612)

def rightDownLeftUp():
	api.SetMotorValue(9,466)
	api.SetMotorValue(6,558)
	api.SetMotorValue(14,558)

	api.SetMotorValue(10,611)
	api.SetMotorValue(5,412)
	api.SetMotorValue(13,412)	

def leftDownRightUp():
	api.SetMotorValue(10,558)
	api.SetMotorValue(5,466)
	api.SetMotorValue(13,466)

	api.SetMotorValue(9,412)
	api.SetMotorValue(6,611)
	api.SetMotorValue(14,611)

def leftUpRightUp():
	api.SetMotorValue(9,466)
	api.SetMotorValue(10,558)

	api.SetMotorValue(6,611)
	api.SetMotorValue(14,611)
	api.SetMotorValue(13,412)
	api.SetMotorValue(5,412)

def leftDownRightDown():
	api.SetMotorValue(9,412)
	api.SetMotorValue(10,611)

	api.SetMotorValue(6,558)
	api.SetMotorValue(14,558)
	api.SetMotorValue(13,466)
	api.SetMotorValue(5,466)

def tailStrike():
	# api.SetMotorValue(16, 512)
	# time.sleep(.1)
	api.SetMotorValue(17, 512)
	time.sleep(.1)
	api.SetMotorValue(18, 512)

	time.sleep(.2)

	# api.SetMotorValue(16, 600)
	api.SetMotorValue(17, 700)
	api.SetMotorValue(18, 700)

	time.sleep(.3)

def pinch():
	api.SetMotorValue(1,592)
	api.SetMotorValue(2,425)

	time.sleep(.2)

	api.SetMotorValue(1,421)
	api.SetMotorValue(2,595)

	time.sleep(.3)

def init():
	api.SetMotorValue(18,700)
	api.SetMotorValue(17,700)
	api.SetMotorValue(16,512)

	api.SetMotorValue(6,512)
	api.SetMotorValue(10,512)
	api.SetMotorValue(14,512)

	api.SetMotorValue(5,512)
	api.SetMotorValue(9,512)
	api.SetMotorValue(13,512)

	time.sleep(.3)

	pinch()

def turnRight(speed):
	if speed < 1:
		speed = 1
	if speed > 3:
		speed = 3

	leftDownRightDown()
	leftSideBackwards()
	rightSideForwards()
	
	time.sleep(.1 * speed)

	leftUpRightUp()
	rightSideBackwards()
	leftSideForwards()
	
	time.sleep(.1 * speed)

def turnLeft(speed):
	if speed < 1:
		speed = 1
	if speed > 3:
		speed = 3

	leftDownRightDown()
	rightSideBackwards()
	leftSideForwards()
	
	time.sleep(.1 * speed)

	leftUpRightUp()	
	leftSideBackwards()
	rightSideForwards()
	
	time.sleep(.1 * speed)
	
def walkForwards(speed):
	if speed < 1:
		speed = 1
	if speed > 3:
		speed = 3

	leftSideBackwards()
	rightSideForwards()
	
	time.sleep(.1 * speed)
	
	rightDownLeftUp()
	
	time.sleep(.1 * speed)
	
	leftSideForwards()
	rightSideBackwards()
	
	time.sleep(.1 * speed)
	
	leftDownRightUp()
	
	time.sleep(.1 * speed)
	
def walkBackwards(speed):
	if speed < 1:
		speed = 1
	if speed > 3:
		speed = 3

	rightSideBackwards()
	leftSideForwards()
	
	time.sleep(.1 * speed)
	
	rightDownLeftUp()
	
	time.sleep(.1 * speed)
	
	leftSideBackwards()
	rightSideForwards()
	
	time.sleep(.1 * speed)
	
	leftDownRightUp()
	
	time.sleep(.1 * speed)
