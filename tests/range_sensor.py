import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

TRIG = 23
ECHO = 24

print "Distance Measurement In Progress"

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

GPIO.output(TRIG, False)
print "Waiting For Senor To Settle"
time.sleep(2)
count = 0
while(count < 7):
	GPIO.output(TRIG, True)
	time.sleep(0.0001)
	GPIO.output(TRIG, False)

	while GPIO.input(ECHO)==0:
	 pulse_start=time.time()

	while GPIO.input(ECHO)==1:
 	 pulse_end = time.time()

	pulse_duration = pulse_end - pulse_start

	distance = pulse_duration * 17150

	distance = round(distance, 2)

	print "Distance:" , distance, "cm"
	time.sleep(1)
	count = count + 1
GPIO.cleanup()