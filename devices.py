import sqlite3
from utils import db

def list():
	with db('ha.db') as c:
		return c.cursor().execute('SELECT * FROM devices').fetchall()
