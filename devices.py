import sqlite3
from utils import db

def list():
	with db('ha.db') as c:
		return c.cursor().execute('SELECT * FROM device').fetchall()
def create(bus_id, name, addr):
        with db('ha.db') as c:
		c.execute('insert into device(bus_id,name,address) values (?,?,?)', (bus_id, name, addr))
def address(id):
	with db('ha.db') as c:
		return c.cursor().execute('SELECT address FROM device WHERE id=?', (id,)).fetchall()[0][0]

def name(id):
	with db('ha.db') as c:
		return c.cursor().execute('SELECT name FROM device WHERE id=?', (id,)).fetchall()[0][0]
def bus(id):
	with db('ha.db') as c:
		return c.cursor().execute('SELECT bus_id FROM device WHERE id=?', (id,)).fetchall()[0][0]

def update(id,bus_id, name, addr):
	with db('ha.db') as c:
		if bus_id is not None:
			c.execute('update device set bus_id=? where id=?',(bus_id,id))
		if name is not None:
			print "update:"+str(name) + " id " + str(id)
			c.execute('update device set name=? where id=?',(name,id))
		if addr is not None:
			c.execute('update device set address=? where id=?',(addr,id))
def delete(id):
	with db('ha.db') as c:
		c.execute('delete from device where id=?',(id,))
	