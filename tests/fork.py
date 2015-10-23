import os
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

GPIO.setup(22,GPIO.IN,pull_up_down=GPIO.PUD_UP)

raw_input("Press enter when ready\n>")

print "Waiting for falling edge"
print "During this waiting time, program is not wasting resources by pollling for a button press.\n"

try:
	GPIO.wait_for_edge(22,GPIO.FALLING)
	pid = os.fork()
	if pid == 0 :
		os.execlp('python','python','range_sensor.py')
	else:
		os.wait()
		print "finished running range_sensor.py"
except KeyboardInterrupt:
	GPIO.cleanup()
