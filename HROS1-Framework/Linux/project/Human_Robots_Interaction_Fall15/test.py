#!/usr/bin/python3
import sys, os, ctypes, time
import api

if api.Initialize():
    print("Initialized")
else:
    print("Initialization failed")
    sys.exit(1)

api.ServoStartup()
print("Battery voltage:", api.BatteryVoltLevel() / 10)

time.sleep(2)
#front right 4
print api.GetMotorValue(13)
print api.GetMotorValue(9)
print api.GetMotorValue(13)
#print api.GetMotorValue(4)
#print api.GetMotorValue(12)
#back right 12
#value = int(input("Turn back right to : " ))
#api.SetMotorValue(12,value)

api.ServoShutdown()
print('Finished')
