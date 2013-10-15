import cStringIO
import web
import json
import mimerender
import device
import devices

rest_render_xml = lambda **args: json.dumps(args)
rest_render_json = lambda **args: json.dumps(args)
rest_render_html = lambda **args: json.dumps(args)
rest_render_txt = lambda **args: json.dumps(args)

urls = (
	"/rest/device", "DeviceRestAPI",
        "/rest/devices", "DevicesRestAPI",
	"/devices.html", "Devices",
	"/index.html", "Index",
	"/", "Index"

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
                default = 'html',
                html = rest_render_html,
                xml  = rest_render_xml,
                json = rest_render_json,
                txt  = rest_render_txt
        )
        def GET(self): # gets the status of device: currently in bootloader/running state
                data = web.input()
                return {'status': device.probe(int(data['addr']))}
        def POST(self):
		try:
			log = cStringIO.StringIO()
			data = web.input()
			device.firmware_erase(int(data['addr']), 0x8200*2, log)
			return {'status': device.firmware_upload(int(data['addr']), data['firmware'].file, 0x8200*2, log), 'log': log }
		except IOError,err:
			return RestError(str(err))
        def PUT(self):
		data = web.input()
                if data['launch_addr']:
                        return {'status': device.launch(int(data['launch_addr']))}
                if data['discover_addr']:
                        return {'status': device.discover(int(data['discover_addr']))}


# devices representation, this simply facade to devices.py api
class DevicesRestAPI:
        @mimerender(
                default = 'html',
                html = rest_render_html,
                xml  = rest_render_xml,
                json = rest_render_json,
                txt  = rest_render_txt
        )
        def GET(self): # gets the status of device: currently in bootloader/running state
                return {'devices' : devices.list()}

class Devices:
	def GET(self): # entry point into application, it is using template to render index.
		return render.devices(render.header(2),render.footer())

class Index:
	def GET(self): # entry point into application, it is using template to render index.
		return render.index(render.header(1),render.footer())

if __name__ == "__main__":
        app.run()

