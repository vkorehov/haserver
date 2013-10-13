import smbus
import os
import time
from intelhex import IntelHex

ih1 = IntelHex()
ih1.loadhex("capsens.X.production.hex")
ih1d = ih1.todict()     # dump contents to pydict
for a in range(0,0x800,16):
	d = [(hex(ih1d[aa]) if aa in ih1d else "0xXX") for aa in range(a,a+16)]
        print "mem @:"+hex(a/2) + " data:"+str(d)

ih2 = IntelHex()
ih2.loadhex("memory.hex")
ih2d = ih2.todict()     # dump contents to pydict

for a in range(0,0x200,16):
	aw = a / 2
	d = [(ih2d[aa] if aa in ih2d else 0) for aa in range(a,a+16)]
	dd = [(ih2d[aa] if aa in ih2d else 0) for aa in range(a+0x400,a+0x400+16)]
	print "verifying block (expected) @:"+hex(aw) + " data:"+(':'.join("%02x" % c for c in d))
	print "verifying block (actual  ) @:"+hex(aw+0x200) + " data:"+(':'.join("%02x" % c for c in dd))
	for aa in range(0,16):
		if (a + aa in ih2d) and d[aa] != dd[aa]:
			raise IOError('Data Differs')
