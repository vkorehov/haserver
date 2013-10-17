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

def _bus_read(c,bus):
        status = GPIO.input(29)
        c.cursor().execute('UPDATE bus set status = ? WHERE id = ?',(status,bus))
        return status

def _bus_write(c,bus,value):
        GPIO.output(28,value)
        status = GPIO.input(29)
	c.cursor().execute('UPDATE bus set status = ? WHERE id = ?',(status,bus))
# poweron on startup
try:
	with db('ha.db') as c:
		_bus_write(c,1,1)
except Exception,ex:
        print "failed to initially poweron bus, error:"+str(ex)

#pediodic timer to update periodically our main bus
def _bus_checks():
	try:
		with db('ha.db') as c:
			_bus_read(c,1)
			_bus_read(c,2)
			_bus_read(c,3)
	except Exception, ex:
		print "exception happened during periodic bus status check:"+str(ex)
	threading.Timer(5, _bus_checks).start()

_bus_checks()

def update(bus, onoff):
	with db('ha.db') as c:
		_bus_write(c,bus, onoff)

def history(bus,interval,steps,after):
        with db('ha.db') as c:
		_bus_read(c,bus)
		t = int(time.time())
		newafter = c.cursor().execute('SELECT MAX(last_updated) FROM bus_history WHERE bus_id=?',(bus,)).fetchall()[0];
		if newafter == after:
			return []
		return {'history':history2plot(t, interval, steps, c.cursor().execute('SELECT last_updated,status FROM bus_history WHERE bus_id=? AND last_updated >= ? ORDER BY id DESC',(bus,t - interval)).fetchall()),'after': newafter}
