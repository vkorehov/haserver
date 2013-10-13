import smbus
import os
import time
from intelhex import IntelHex

bus = smbus.SMBus(1)
# I2C address for device to programm
i2c_addr = 0x10
flash_erase_block = 0x20
flash_write_block = 0x08
total_retries_count = 0
def flash_launch():
	bus.read_word_data(i2c_addr, 0x06)

def flash_erase(addr):
	global total_retries_count
	retries_count = 0
	while True:
		if retries_count > 100:
			raise IOError('too many retries while communication with device')
		try:			
			bus.write_word_data(i2c_addr, 0x01, addr)        
			if bus.read_word_data(i2c_addr, 0x01) != addr:
				retries_count += 1
				continue
			bus.read_word_data(i2c_addr, 0x04)
			if bus.read_word_data(i2c_addr, 0x01) != (addr+flash_erase_block):
				retries_count += 1
				continue
			total_retries_count += retries_count
			return
		except IOError,err:
			retries_count += 1
			continue;

def flash_upload(addr, data):
        global total_retries_count
	retries_count = 0
	while True:
                if retries_count > 100:
                        raise IOError('too many retries while communication with device')
		try:
	                # upload data to internal buffer!
        	        bus.write_i2c_block_data(i2c_addr, 0x02, data)
			# set address
        	        bus.write_word_data(i2c_addr, 0x01, addr)
               		if bus.read_word_data(i2c_addr, 0x01) != addr:
				retries_count += 1
                	        continue
			# write to flash
			bus.read_word_data(i2c_addr, 0x05)
               		if bus.read_word_data(i2c_addr, 0x01) != (addr+flash_write_block):
				retries_count += 1
                       		continue
			total_retries_count += retries_count
			return
                except IOError,err:
                        retries_count += 1
                        continue;

def flash_download(addr):
        global total_retries_count
	retries_count = 0
        while True:
                if retries_count > 100:
                        raise IOError('too many retries while communication with device')
                try:
	                bus.write_word_data(i2c_addr, 0x01, addr)
	                if bus.read_word_data(i2c_addr, 0x01) != addr:
				retries_count += 1
        	                continue
                	data = bus.read_i2c_block_data(i2c_addr, 0x03)
                	if bus.read_word_data(i2c_addr, 0x01) != (addr+flash_write_block):
				retries_count += 1
                       		continue
			del data [flash_write_block*2:]
                	total_retries_count += retries_count
			return data
                except IOError,err:
                        retries_count += 1
                        continue;

def erase_device(size):
	# Reset address pointer in the device
	aw = 0x200
	while aw*2 < size:
		#erase 0x20 bytes of flash
		if aw >= 0x4000 and aw < 0x8000:
			# skip non-implemented memory
			aw += flash_erase_block
			continue
		print 'Erasing address:' + hex(aw) + ' to ' + hex(aw+flash_erase_block)
		flash_erase(aw)
		aw += 32

def upload_firmware(filename, size):
	ih = IntelHex()
	ih.loadhex(filename)
	ihd = ih.todict()     # dump contents to pydict
	skiprange = False
	for a in range(0,size,flash_write_block*2): # PIC16F
		skiprange = True
		for aa in range(a,a+flash_write_block*2):
			if aa in ihd:
				skiprange = False
		if skiprange:
			continue;
                # only 14bit data with leading high byte, mask unused bits away, if hex file had no entry for some byte them, put zeres
                d = [(ihd[aa] if aa in ihd else 0) for aa in range(a,a+flash_write_block*2)]
		
		aw = a/2 # config space is mapped AS-IS

		if aw >= 0x8000: # skip programming of config space
			continue;
                if aw >= 0x4000:
                        raise IOError('hex file is too large to fit into memory range')

		if aw < 0x80000: # skip programming of config space
			print "programming block @:"+hex(aw) + " data:"+(':'.join("%02x" % c for c in d))
			flash_upload(aw,[c for c in d])		
		aw += flash_write_block

        skiprange = False
        for a in range(0,size,flash_write_block*2): # PIC16F
                skiprange = True
                for aa in range(a,a+flash_write_block*2):
                        if aa in ihd:
                                skiprange = False
                if skiprange:
                        continue;
		# only 14bit data with leading high byte, mask unused bits away, if hex file had no entry for some byte them, put zeres
                d = [(ihd[aa] if aa in ihd else 0) & 0x3f if a % 2 == 1 else (ihd[aa] if aa in ihd else 0)  for aa in range(a,a+flash_write_block*2)]

                aw = a/2 # config space is mapped AS-IS
		if aw >= 0x8000:
			# skip verification of config space
			continue

                print "verifying block (expected) @:"+hex(aw) + " data:"+(':'.join("%02x" % c for c in d)),
		dd = flash_download(aw)
		#print "verifying block (actual  ) @:"+hex(aw) + " data:"+(':'.join("%02x" % c for c in dd))
                aw += flash_write_block		
		for av in range(a,a+flash_write_block*2,2):
			if (av in ihd) and ((dd[av - a] != d[av - a]) or dd[av - a + 1] & 0x3f != d[av - a + 1]):
				fa = aw-flash_write_block + av/2				
				raise IOError("device flash data is different from expected @"+hex(aw-flash_write_block)+\
							", it is:"+hex(dd[av-a])+","+hex(dd[av-a+1])+" while should be:"+hex(d[av-a])+","+hex(d[av-a+1]))
		print "OK"
 

erase_device(0x8200*2)
upload_firmware('capsens.X.production.hex', 0x8200*2)
#capsens.X.production.hex
#upload_firmware('capsens.X.production.hex', 0x8200*2)
print "Total retries:" + str(total_retries_count)
flash_launch()
