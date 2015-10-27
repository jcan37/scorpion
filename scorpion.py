__author__ = 'jeff'

import RPi.GPIO as GPIO
import time
import threading
import logging

THRESHOLD = 20
TIME_PER_SAMPLE = 0.1
STARTING_WEIGHT = 1.1
SAMPLE_WEIGHT = 0.125

LED = 22
TRIG = 23
ECHO = 24

running = True
logging.basicConfig(level=logging.DEBUG, 
                    format='[%(levelname)s] (%(threadName)-10s) %(message)s')

def gpio_setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(LED, GPIO.OUT)
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)
    GPIO.output(TRIG, False)

def object_detector():
    logging.debug('Spawning object detector...')
    gpio_setup()
    distance = STARTING_WEIGHT * THRESHOLD
    while running:
        distance = SAMPLE_WEIGHT * sample_distance() + \
                   (1 - SAMPLE_WEIGHT) * distance
        if distance < THRESHOLD:
            turn_on_led()
        else:
            turn_off_led()
        time.sleep(TIME_PER_SAMPLE)
    GPIO.cleanup()

def sample_distance():
    GPIO.output(TRIG, True)
    time.sleep(0.0001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO) == 0:
        pass
    pulse_start=time.time()

    while GPIO.input(ECHO) == 1:
        pass
    pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    return distance

def turn_on_led():
    logging.debug('LED on')
    GPIO.output(LED, GPIO.HIGH)

def turn_off_led():
    logging.debug('LED off')
    GPIO.output(LED, GPIO.LOW)

if __name__ == '__main__':
    object_detector_thread = threading.Thread(target=object_detector)
    object_detector_thread.setDaemon(True)
    object_detector_thread.start()
    while True:
        cin = raw_input('> ')
        cin = cin.lower()
        if cin == 'exit' || cin == 'quit' || cin == 'q':
            running = False
            break
