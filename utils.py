import sqlite3
import contextlib

def DictFactory(cursor, row):
    d = {}
    for idx,col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

@contextlib.contextmanager
def db(name):
        con = sqlite3.connect(name)
	#con.row_factory = DictFactory
        try:
                yield con
        finally:
                con.close()

