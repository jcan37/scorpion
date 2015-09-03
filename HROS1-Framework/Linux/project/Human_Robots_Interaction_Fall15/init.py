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
api.SetMotorValue(18,700)
api.SetMotorValue(17,700)
api.SetMotorValue(16,700)

api.SetMotorValue(6,512)
api.SetMotorValue(10,512)
api.SetMotorValue(14,512)

api.SetMotorValue(5,512)
api.SetMotorValue(9,512)
api.SetMotorValue(13,512)

time.sleep(.5)

api.SetMotorValue(1,592)
api.SetMotorValue(2,425)

time.sleep(.2)

api.SetMotorValue(1,421)
api.SetMotorValue(2,595)

time.sleep(1)

while True:
	cin = raw_input('')
	cin = cin.lower()
	if cin == 'sleep':
		break

api.ServoShutdown()
print('Finished')
