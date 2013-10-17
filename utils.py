import sqlite3
import contextlib
import time
import random

def DictFactory(cursor, row):
    d = {}
    for idx,col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

@contextlib.contextmanager
def db(name):
        con = sqlite3.connect(name)
        try:
                yield con
        finally:
		con.commit()
                con.close()

def history2plot(t,interval, steps, data):
	print str(data)
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
				output.append(0)
			else:
				if lastval is None:
					rnd = random.randint(0, len(last))
					lastval = last[0 if rnd >= len(last) else rnd]
				else:
					for v in last:
						if v != lastval:
							lastval = v
							break;						
				#print "lastval="+str(lastval)+" vals="+str(last)
				output.append(1 if lastval > 0 else -1)
			last = []
		i += 1
	output.reverse()
	return output
