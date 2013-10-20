import RPi.GPIO as GPIO
import threading
import time
from utils import db
from utils import history2plot
from time import sleep
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(28, GPIO.OUT)
GPIO.setup(29, GPIO.IN)

status = GPIO.input(29)
print "status:"+str(status)
GPIO.output(28,1)
status = GPIO.input(29)
print "status off:"+str(status)

