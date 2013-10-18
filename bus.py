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

bus_lock = threading.RLock()

def _bus_read(c,bus):	
        status = GPIO.input(29)
	# bus is inverted
	if status:
		status = 0
	else:
		status = 1
        c.execute('UPDATE bus set status = ? WHERE id = ?',(status,bus))
        return status

def _bus_write(c,bus,value):
	if value:
		value = 0
	else:
		value = 1
	print 'writing to port:'+str(value)
	GPIO.output(28,value)
	status = GPIO.input(29)
	if status:
		value = 0
	else:
		value = 1
	c.execute('UPDATE bus set status = ? WHERE id = ?',(status,bus))
# poweron on startup
try:
	with db('ha.db') as c:
		_bus_write(c,1,1)
except Exception,ex:
        print "failed to initially poweron bus, error:"+str(ex)

#pediodic timer to update periodically our main bus
def _bus_checks():
	while True:
		time.sleep(5)
		try:
			with bus_lock:
				with db('ha.db') as c:
					bus1 = _bus_read(c,1)
					if not bus1:
						_bus_write(c,1,1)
					bus2 = _bus_read(c,2)
					if not bus2:
						_bus_write(c,2,1)
					bus3 = _bus_read(c,3)
					if not bus3:
						_bus_write(c,3,1)
		except KeyboardInterrupt:
			break
		except Exception,ex:
			print "exception happened during periodic bus status check:"+str(ex)
th = threading.Thread(target=_bus_checks)
th.daemon = True
th.start()

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
		data = c.cursor().execute('SELECT last_updated,status FROM bus_history WHERE bus_id=? AND last_updated >= ? ORDER BY id DESC',(bus,t - interval)).fetchall()
		data.insert(0, [t,_bus_read(c,bus)])
		h = history2plot(t, interval, steps, data)
		return {'history':h,'after': t}

def toggle(bus):
	with bus_lock:
		try:
			with db('ha.db') as c:
				_bus_write(c,bus,0)
			time.sleep(5)
		finally:
			with db('ha.db') as c:
				_bus_write(c,bus,1)
