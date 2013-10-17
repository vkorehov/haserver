PRAGMA foreign_keys = ON;
CREATE TABLE bus(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, status INTEGER);
INSERT INTO bus(id,name,status) VALUES(1,'5V',0);
INSERT INTO bus(id,name,status) VALUES(2,'12V',0);
INSERT INTO bus(id,name,status) VALUES(3,'220V',0);
CREATE TABLE bus_history(id INTEGER PRIMARY KEY AUTOINCREMENT,
			status INTEGER,
			bus_id INTEGER REFERENCES bus(id),
			last_updated INTEGER);
CREATE TRIGGER bus_status_trigger UPDATE OF status ON bus WHEN new.status <> old.status
  BEGIN
    INSERT INTO bus_history(status,bus_id,last_updated) VALUES(new.status,old.id,strftime('%s', 'now'));
    DELETE FROM bus_history WHERE id < (SELECT MAX(id) - 512 FROM bus_history);
  END;

CREATE TABLE buses(id INTEGER PRIMARY KEY,name TEXT,bus_id INTEGER REFERENCES bus(id));
INSERT INTO buses(id,name,bus_id) VALUES(1,'5V',1);
INSERT INTO buses(id,name,bus_id) VALUES(2,'12V',2);
INSERT INTO buses(id,name,bus_id) VALUES(4,'220V',3);
INSERT INTO buses(id,name,bus_id) VALUES(3,'5V/12V',1);
INSERT INTO buses(id,name,bus_id) VALUES(5,'5V/220V',1);
INSERT INTO buses(id,name,bus_id) VALUES(7,'5V/12V/220V',1);

CREATE TABLE device(id INTEGER PRIMARY KEY AUTOINCREMENT,
		bus_id INTEGER REFERENCES buses(id),
		name TEXT,
		address INTEGER);
INSERT INTO device(name,bus_id,address) VALUES('Switch A',1,16);
INSERT INTO device(name,bus_id,address) VALUES('Switch B',1,20);
INSERT INTO device(name,bus_id,address) VALUES('Raspbery PI',1,64);
INSERT INTO device(name,bus_id,address) VALUES('Dimmer 1',1,30);
INSERT INTO device(name,bus_id,address) VALUES('Dimmer 2',1,31);
INSERT INTO device(name,bus_id,address) VALUES('Dimmer 3',1,32);
INSERT INTO device(name,bus_id,address) VALUES('Dimmer 4',1,33);
INSERT INTO device(name,bus_id,address) VALUES('Dimmer 5',1,34);
INSERT INTO device(name,bus_id,address) VALUES('Water Pump',1,50);
INSERT INTO device(name,bus_id,address) VALUES('Water Valve 1',1,51);
INSERT INTO device(name,bus_id,address) VALUES('Water Valve 2',1,52);
INSERT INTO device(name,bus_id,address) VALUES('Water Valve 3',1,53);

