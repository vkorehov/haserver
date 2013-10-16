PRAGMA foreign_keys = ON;
CREATE TABLE bus(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, status INTEGER);
INSERT INTO bus(id,name,status) VALUES(1,'main',0);
CREATE TABLE bus_history(id INTEGER PRIMARY KEY AUTOINCREMENT,
			status INTEGER,
			bus_id INTEGER REFERENCES bus(id),
			last_updated DATETIME);
CREATE TRIGGER bus_status_trigger UPDATE OF status ON bus WHEN new.status <> old.status
  BEGIN
    INSERT INTO bus_history(status,bus_id,last_updated) VALUES(new.status,old.id,CURRENT_TIMESTAMP);
    DELETE FROM bus_history WHERE id < (SELECT MAX(id) - 512 FROM bus_history);
  END;

CREATE TABLE device(id INTEGER PRIMARY KEY AUTOINCREMENT,
		bus_id INTEGER REFERENCES bus(id),
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

