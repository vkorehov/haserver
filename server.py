import cStringIO
import web
import json
import mimerender
import device
import devices
import bus
import re
import logging

rest_render_xml = lambda **args: json.dumps(args)
rest_render_json = lambda **args: json.dumps(args)
rest_render_html = lambda **args: json.dumps(args)
rest_render_txt = lambda **args: json.dumps(args)

urls = (
       "/rest/bus",      	"BusRestAPI",
	"/rest/device",  	"DeviceRestAPI",
       "/rest/devices", 	"DevicesRestAPI",
	"/devices.html", 	"Devices",
	"/index.html",   	"Index",
	"/",             	"Index"
)

app = web.application(urls, globals())
mimerender = mimerender.WebPyMimeRender()
render = web.template.render('templates/', cache=False)

class RestError(web.HTTPError):
	def __init__(self, err):
		status = '501 ' + err
		web.HTTPError.__init__(self, status)

# device representation, this simply facade to device.py api
class DeviceRestAPI:
        @mimerender(
                default = 'json',
                html = rest_render_html,
                xml  = rest_render_xml,
                json = rest_render_json,
                txt  = rest_render_txt
        )
        def GET(self): # gets the status of device: currently in bootloader/running state
		try:
			data = web.input()
			return {'status': device.probe(int(data['addr']))}
		except Exception,ex:
			return {'status': []}
        def POST(self):
		data = web.input(addr={})
		fdata = web.input(firmware={})
		try:
			if 'launch_addr' in data:
				return {'status': device.launch(int(data['launch_addr']))}
			if 'discover_addr' in data:
				return {'status': device.discover(int(data['discover_addr']))}
			log = cStringIO.StringIO()
			data = web.input()
			device.firmware_erase(int(data['addr']), 0x8200*2, log)
			print log
			log = cStringIO.StringIO()
			return {'status': device.firmware_upload(int(data['addr']), fdata['firmware'].file, 0x8200*2, log), 'log': log }
			print log
		except Exception,err:
			logging.exception(err)
			return RestError(str(err))

# devices representation, this simply facade to devices.py api
class DevicesRestAPI:
        @mimerender(
                default = 'json',
                html = rest_render_html,
                xml  = rest_render_xml,
                json = rest_render_json,
                txt  = rest_render_txt
        )
        def GET(self): # gets the status of device: currently in bootloader/running state
		try:
			return {'devices' : devices.list()}
		except Exception,ex:
			logging.exception(ex)
			return {'devices' : []}
	def POST(self):
		data = web.input()
		if 'create' in data:
			return devices.create(data.bus_id, data.name, data.addr)
		if int(data.column) == 1: # bus_id
			devices.update(data.row_id, data.value, None, None)
			return devices.bus(data.row_id)
		if int(data.column) == 2: # name
			devices.update(data.row_id, None, data.value, None)
			return devices.name(data.row_id)
		if int(data.column) == 3: # address
			m = re.match('(0x)?([0-9a-fA-F]{1,2})', data.value)
			if m is not None:
				a = m.groups()[-1].upper()
				devices.update(data.row_id, None, None, int(a, 16))
			return "%X" % devices.address(data.row_id)
	def DELETE(self):
		data = web.input()
		devices.delete(data.id)

# devices representation, this simply facade to bus.py api
class BusRestAPI:
        @mimerender(
              default = 'json',
              html = rest_render_html,
              xml  = rest_render_xml,
              json = rest_render_json,
              txt  = rest_render_txt
        )
        def GET(self): # gets the status of device: currently in bootloader/running state
		data = web.input()
		try:
                	return bus.history(int(data['bus']), int(data['interval']), int(data['steps']), int(data['after']))
		except Exception,ex:
			logging.exception(ex)
			return {'history' : []}
	def POST(self):
		data = web.input()
		try:
			if 'toggle_bus' in data:
				bus.toggle(data.toggle_bus)
			else:
				raise IOError('Unknown parameters')
		except Exception,err:
			logging.exception(err)
			return RestError(str(err))
class Devices:
	def GET(self): # entry point into application, it is using template to render index.
		return render.devices(render.header(2),render.footer())
class Index:
	def GET(self): # entry point into application, it is using template to render index.
		return render.index(render.header(1),render.footer())

if __name__ == "__main__":
        app.run()

