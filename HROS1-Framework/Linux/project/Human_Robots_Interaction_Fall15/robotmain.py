import movements
import api
import time
import threading
import logging
import sys
import serial
from random import randrange

try:
	msp = serial.Serial('/dev/ttyACM0', 9600)
except serial.SerialException:
	print 'I need my eyes! Plug the MSP in and try again.'
	sys.exit(1)

running = True
speed = 2
validator = 0
backup = False
rightTurn = False
logging.basicConfig(level=logging.DEBUG, 
                    format='[%(levelname)s] (%(threadName)-10s) %(message)s')

def usage():
	print "Commands:"
	print "  sleep   -  Put me to sleep."
	print "  slower  -  Make me move faster."
	print "  faster  -  Make me move slower."

def startup():
	if api.Initialize():
		print "I'm awake!"
	else:
		print "I'm too tired. Maybe later."
		sys.exit(1)
	api.ServoStartup()
	power = api.BatteryVoltLevel() / 10
	if power < 11:
		print 'Need energy to move, feed me! Replace my battery or charge it.'
		sys.exit(1)
	# print 'Battery voltage: ' + str(api.BatteryVoltLevel() / 10)
	usage()
	time.sleep(2)
	movements.init()	

def shutdown():
	api.ServoShutdown()
	print "I'm exhausted. Time to sleep..."

def serializer():
	global running
	global msp
	global validator
	global backup
	logging.debug('Spawning serial thread...')
	while running:
		value = 'f'
		try:
			value = msp.read(1)
		except serial.SerialException:
			print 'Failed to read MSP. Attempting to reconnect...'
			try:
				msp = serial.Serial('/dev/ttyACM0', 9600)
			except serial.SerialException:
				print 'Failed to reconnect. I need my eyes! Plug the MSP in and try again.'
				running = False
				sys.exit(1)
		if value == 'b':
			validator += 1
		else:
			validator = 0
		if validator >= 5:
			backup = True

def runner():
	global running
	logging.debug('Spawning action thread...')
	while running:
		wander()

def randomTurn():
	global speed
	global backup
	global validator
	randTurn = randrange(0, 2)
	backup = True
	iterations = 0
	while backup:
		randDuration = randrange(2, 7) * 2
		# print 'Turning ' + str(randDuration) + ' steps'
		iterations += randDuration
		backup = False
		validator = 0
		for x in range(0, randDuration):
			if randTurn > 0:
				rightTurn = True
				# print 'Turning right'
				movements.turnRight(speed)
			else:
				rightTurn = False
				# print 'Turning left'
				movements.turnLeft(speed)
		if iterations > 12:
			for y in range(0, 2):
				movements.pinch()
			movements.tailStrike()
			# print 'Intimidate'
			print 'Hissss, get out the way!'
			break

def intuitiveTurn():
	global speed
	global backup
	global validator
	backup = True
	iterations = 0
	while backup:
		randDuration = randrange(2, 5) * 2
		# print 'Turning ' + str(randDuration) + ' steps'
		iterations += randDuration
		backup = False
		validator = 0
		for x in range(0, randDuration):
			if rightTurn:
				# print 'Turning right'
				movements.turnRight(speed)
			else:
				# print 'Turning left'
				movements.turnLeft(speed)
		if iterations > 8:
			for y in range(0, 2):
				movements.pinch()
			movements.tailStrike()
			# print 'Intimidate'
			print 'Hissss, get out the way!'
			break

def wander():
	global speed
	global backup
	global validator
	randDuration = randrange(2, 17) * 4
	# print 'Walking a max of ' + str(randDuration) + ' steps'
	randTurn = True
	for x in range(0, randDuration):
		if backup:
			if x < 8:
				randTurn = False
				break
			else:
				movements.pinch()
				movements.tailStrike()
				# print 'Intimidate'
				for y in range (0, 4):
					movements.walkBackwards(speed)
					# print 'Walking backwards'
			backup = False
			validator = 0
			break
		else:
			if not running:
				break
			movements.walkForwards(speed)
			# print 'Walking forwards'
	if randTurn:
		randomTurn()
	else:
		intuitiveTurn()

if __name__ == '__main__':
	startup()

	serial_thread = threading.Thread(target=serializer)
	serial_thread.setDaemon(True)
	serial_thread.start()

	action_thread = threading.Thread(target=runner)
	action_thread.setDaemon(True)
	action_thread.start()

	while True:
		cin = raw_input('')
		cin = cin.lower()
		if cin == 'exit' or cin == 'e' or cin == 'quit' or cin == 'q' or cin == 'die' or cin == 'd' or cin == 'sleep':
			running = False
			break
		if cin == 'faster' or cin == 'fast' or cin == 'f':
			if speed > 1:
				speed -= 1
				print "Alright boss, I'll speed it up."
			else:
				print "Can't. Move. Any. Faster."
		if cin == 'slower' or cin == 'slow' or cin == 's':
			if speed < 3:
				speed += 1
				print "Alright boss, I'll slow it down."
			else:
				print "I refuse to move that slow. You might as well put me to sleep."

	shutdown()
