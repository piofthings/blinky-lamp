
#!/usr/bin/env python

from http.server import BaseHTTPRequestHandler, HTTPServer
from cgi import parse_header, parse_multipart
from urllib.parse import parse_qs

import colorsys
import time

hostName = "localhost"
hostPort = 9000

try:
    import numpy as np
except ImportError:
    exit("This script requires the numpy module\nInstall with: sudo pip install numpy")

from blinkt import set_clear_on_exit, set_pixel, show, set_brightness, clear

set_clear_on_exit()

class MyServer(BaseHTTPRequestHandler):
	def do_GET(self):
		self.send_response(200)
		self.send_header("Content-type", "text/html")
		self.end_headers()
		self.wfile.write(bytes("<html><head><title>Blinky Lamp</title></head>", "utf-8"))
		self.wfile.write(bytes("<body><p>Turn Blinky on or off</p>", "utf-8"))
		self.wfile.write(bytes("<form action='/' method='post'>", "utf-8"))
		self.wfile.write(bytes("<input type='hidden' value='blue' name='color'>", "utf-8"))
		self.wfile.write(bytes("<input type='hidden' value='1.0' name='intensity'>", "utf-8"))
		self.wfile.write(bytes("<input type='submit' value='on' name='state'>", "utf-8"))
		self.wfile.write(bytes("<input type='submit' value='off' name='state'>", "utf-8"))
		self.wfile.write(bytes("</body></html>", "utf-8"))
		self.wfile.write(bytes("</form>", "utf-8"))

	def do_POST(self):
		ctype, pdict = parse_header(self.headers['content-type'])
		if ctype == 'multipart/form-data':
			postvars = parse_multipart(self.rfile, pdict)
		elif ctype == 'application/x-www-form-urlencoded':
			length = int(self.headers['content-length'])
			postvars = parse_qs(self.rfile.read(length), keep_blank_values=1)
			print(postvars[b"color"][0].decode("utf-8"))
			print(postvars[b"intensity"][0].decode("utf-8"))
			self.blinkit(postvars[b"color"][0].decode("utf-8"),postvars[b"intensity"][0].decode("utf-8"),postvars[b"state"][0].decode("utf-8"))
		else:
			postvars = {}
		self.send_response(200)
		self.send_header("Content-type", "text/html")
		self.end_headers()
		self.wfile.write(bytes("<html><head><title>Blinky Lamp is </title></head>", "utf-8"))
		self.wfile.write(bytes("<body><p>Turn Blinky on or off</p>", "utf-8"))
		self.wfile.write(bytes("<form action='/' method='post'>", "utf-8"))
		self.wfile.write(bytes("<input type='hidden' value='blue' name='color'>", "utf-8"))
		self.wfile.write(bytes("<input type='hidden' value='1.0' name='intensity'>", "utf-8"))
		self.wfile.write(bytes("<input type='submit' value='on' name='state'>", "utf-8"))
		self.wfile.write(bytes("<input type='submit' value='off' name='state'>", "utf-8"))
		self.wfile.write(bytes("</body></html>", "utf-8"))
		self.wfile.write(bytes("</form>", "utf-8"))


	def make_gaussian(self, fwhm):
		x = np.arange(0, 8, 1, float)
		y = x[:, np.newaxis]
		x0, y0 = 3.5, 3.5
		fwhm = fwhm
		gauss = np.exp(-4 * np.log(2) * ((x - x0) ** 2 + (y - y0) ** 2) / fwhm ** 2)
		return gauss
	
	def blinkit(self,color,intensity,state):
		if state=="on":
			z = 1
			fwhm = 5.0/z
			gauss = self.make_gaussian(fwhm)
			start = time.time()
			y = 4
			for x in range(8):
				h = 0.5
				s = 1.0
				v = gauss[x, y]
				rgb = colorsys.hsv_to_rgb(h, s, v)
				r, g, b = [int(255.0 * i) for i in rgb]
				set_pixel(x, r, g, b)
			set_brightness(1.0)
			show()
			end = time.time()
		elif state=="off":
			clear()
			show()
		return
				
			
myServer = HTTPServer((hostName, hostPort), MyServer)
print(time.asctime(), "Server Starts - %s: %s" % (hostName, hostPort))

try:
	myServer.serve_forever()
except KeyboardInterrupt:
	pass

myServer.server_close()
print(time.asctime(), "Server Stops - %s: %s" % (hostName, hostPort))



