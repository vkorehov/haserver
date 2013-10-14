import cStringIO
import web
import json
import mimerender

rest_render_xml = lambda status: '<status>%s</status>'%status
rest_render_json = lambda **args: json.dumps(args)
rest_render_html = lambda status: '<html><body>%s</body></html>'%status
rest_render_txt = lambda status: status

urls = (
    '/', 'root'
    '/rest/device', 'device'
)
app = web.application(urls, globals())
mimerender = mimerender.WebPyMimeRender()
render = web.template.render('templates/')

# device representation, this simply facade to device.py api
class device:
        @mimerender(
                default = 'html',
                html = rest_render_html,
                xml  = rest_render_xml,
                json = rest_render_json,
                txt  = rest_render_txt
        )
        def GET(self, addr): # gets the status of device: currently in bootloader/running state
                return {'status': device_probe(addr)}
        def POST(self):
		log = cStringIO.StringIO()
                firmware = web.input(firmware={})
                addr = web.input(addr={})
                device_firmware_erase(addr, 0x8200*2, log)
                return {'status': device_firmware_upload(addr, firmware['firmware'].file, 0x8200*2, log), 'log': log }
        def PUT(self):
                launch_addr = web.input(launch={})
                discover_addr = web.input(discover={})
                if launch_addr:
                        return {'status': device_launch(launch_addr)}
                if discover_addr:
                        return {'status': device_discover(discover_addr)}


class root:
	def GET(self): # entry point into application, it is using template to render index.
		model = {'status' : 'OK'}
		return render.index(model)

if __name__ == "__main__":
        app.run()

