import sqlite3
import contextlib
import time
import random

connection = sqlite3.connect('ha.db')
connection.rollback()
connection.close()

#sqlite3.enable_shared_cache(True)

def DictFactory(cursor, row):
    d = {}
    for idx,col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

@contextlib.contextmanager
def db(name):
	con = sqlite3.connect(name,timeout=30,check_same_thread=False,isolation_level='DEFERRED',cached_statements=400)
	try:
		yield con
	finally:
		con.commit()
		con.close()

def history2plot(t,interval, steps, data):
	j = 0
	last = []
	output = []
	period = interval / steps
	i = 0
	lastval = None
	if data:
		lastval = data[0][0]
	while i < steps:
		if j < len(data) and int(data[j][0]) > t - period:
			last.append(int(data[j][1]))
			j += 1
			continue
		else:
			t -= period
			if lastval is None and len(last) == 0:
				output.append('N/A')
			else:
				if lastval is None:
					rnd = random.randint(0, len(last))
					lastval = last[0 if rnd >= len(last) else rnd]
				elif lastval:
					for v in last:
						if v == 0:
							lastval = 0
							break
				else:
					for v in last:
						if v == 1:
							lastval = 1
							break			
				output.append(lastval)
			last = []
		i += 1
	output.reverse()
	return output
