import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

GPIO.setup(22,GPIO.IN,pull_up_down=GPIO.PUD_UP)

raw_input("Press enter when ready\n>")

print "Waiting for falling edge on port 22"

try:
	GPIO.wait_for_edge(22,GPIO.FALLING)
	print "\nFalling edge detected."
except KeyboardInterrupt:
	GPIO.cleanup()
GPIO.cleanup()
