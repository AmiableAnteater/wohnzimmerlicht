import http.server
import socketserver
import os

PORT = 80

web_dir = '/home/pi/NodePrograms/wohnzimmerlicht/build'
os.chdir(web_dir)

Handler = http.server.SimpleHTTPRequestHandler
httpd = socketserver.TCPServer(("", PORT), Handler)
print("serving at port", PORT)
httpd.serve_forever()
