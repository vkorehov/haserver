import smbus
import os
import time

bus = smbus.SMBus(1)
# I2C address for device to programm
i2c_addr = 0x10

def bootloader_enter():
	while True:
		try:
			bus.write_word_data(i2c_addr, 0x01, 0x200)
			if bus.read_word_data(i2c_addr, 0x01) == 0x200:
				print "device discovered @"+hex(i2c_addr)
				break
			time.sleep(1.0)
		except IOError,err:
			continue

bootloader_enter()
