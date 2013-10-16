import sqlite3
from utils import db

def list():
	with db('ha.db') as c:
		return c.cursor().execute('SELECT * FROM device').fetchall()
def create(bus_id, name, addr):
        with db('ha.db') as c:
		c.cursor().execute('insert into device(bus_id,name,address) values (?,?,?)', (bus_id, name, addr))
def update(bus_id, name, addr):
	with db('ha.db') as c:
		if bus_id:
			c.cursor().execute('update device set bus_id=?',(bus_id,))
                if name:
                        c.cursor().execute('update device set name=?',(name,))
                if addr:
                        c.cursor().execute('update device set address=?',(addr,))
