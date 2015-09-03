import sys,os,ctypes,time
import api

if api.Initialize():
	print("Intitialized")
else:
	print("Initialization failed")
	sys.exit(1)

api.ServoStartup()

print("Battery Voltage:",api.BatteryVoltLevel()/10)
time.sleep(2)
#x = int(input("Set motor to : "))

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

for num in range(0,8):
	rightDownLeftUp()

	#leftSideBackwards()
	rightSideForwards()

	time.sleep(.3)
	#7,4,12 down
	leftDownRightUp()
	#move 10,3,11 up

	time.sleep(.3)

	rightSideBackwards()
	#leftSideForwards()

	time.sleep(.3)
	
api.ServoShutdown()
print('Finished')
