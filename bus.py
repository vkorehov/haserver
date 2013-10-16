import RPi.GPIO as GPIO
import threading
from utils import db
from time import sleep
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(28, GPIO.OUT)
GPIO.setup(29, GPIO.IN)

def _bus_read(bus):
        status = GPIO.input(29)
        with db('ha.db') as c:
                c.cursor().execute('UPDATE bus set status = ? WHERE id = ?',(status,bus))
		c.commit()
        return 1 if status == GPIO.HIGH else 0

def _bus_write(bus,value):
        GPIO.output(28,value)
        status = GPIO.input(29)
        with db('ha.db') as c:
                c.cursor().execute('UPDATE bus set status = ? WHERE id = ?',(status,bus))
		c.commit()
# poweron on startup
try:
        _bus_write(1,1)
except Exception,ex:
        print "failed to initially poweron bus, error:"+str(ex)

#pediodic timer to update periodically our main bus
def _bus_checks():
	try:
		_bus_read(1)
	except Exception, ex:
		print "exception happened during periodic bus status check:"+str(ex)
	threading.Timer(5, _bus_checks).start()
_bus_checks()

def status(bus):
	return _bus_read(bus)	


def update(bus, onoff):
	_bus_write(bus, onoff)

def history(bus):
	with db('ha.db') as c:
		c.cursor().execute('SELECT * FROM bus_history WHERE bus_id=?',(bus,))

