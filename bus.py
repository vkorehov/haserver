import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BCM)

GPIO.setup(28, GPIO.OUT)
GPIO.setup(29, GPIO.IN)

lowhi = GPIO.LOW
while True:
	GPIO.output(28, lowhi)
	print 'Level is:'+str(GPIO.input(29))
	if lowhi == GPIO.LOW:
		lowhi = GPIO.HIGH
	else:
		lowhi = GPIO.LOW
	sleep(1.0)
