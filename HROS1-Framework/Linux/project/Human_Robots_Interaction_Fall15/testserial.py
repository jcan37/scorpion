import threading
import serial
import time

ser = serial.Serial("/dev/ttyACM0", 9600)
hits = 0
flag = False
running = True

def serializer():
	global running
	global ser
	global hits
	global flag
	while running:
		if ser.read(1) == 'b':
			hits += 1
		else:
			hits = 0
		if hits > 5:
			flag = True

def detector():
	global running
	global flag
	global hits
	while running:
		time.sleep(0.5)
		if flag:
			hits = 0
			flag = False
			print 'Back up and turn'

serial_thread = threading.Thread(target=serializer)
serial_thread.setDaemon(True)
serial_thread.start()

detect_thread = threading.Thread(target=detector)
detect_thread.setDaemon(True)
detect_thread.start()

while True:
	cin = raw_input('')
	cin = cin.lower()
	if cin == 'exit' or cin == 'quit' or cin == 'q':
		running = False
		break
