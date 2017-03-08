from WS2801 import WS2801Wrapper
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
import sys


pixels = WS2801Wrapper()
PIXEL_COUNT = pixels.count()

clients = []
class SimpleSliderColor(WebSocket):
    def handleMessage(self):
        #print('handling message ' + self.data)
        col = self.data[0]
        if col == 'X':
            pixels.clear()
            pixels.show()
            for client in clients:
                if client != self:
                     client.sendMessage('X') 
            return

       	base_r, base_g, base_b = pixels.get_pixel_rgb(0)
        #print('got values ', base_r, base_g, base_b)
        val = int(self.data[1:])
        if col == "r":
            base_r = val
        elif col == "g":
            base_g = val
        elif col == "b":
            base_b = val
        #print('changing to ', base_r, base_g, base_b)
        for n in range(PIXEL_COUNT):
            pixels.set_pixel_rgb(n, base_r, base_g, base_b)
        pixels.show()
        for client in clients:
            if client != self:
                client.sendMessage(self.data)

    def handleConnected(self):
        #print (self.address, 'connected')
        clients.append(self)
        r, g, b = pixels.get_pixel_rgb(0)
        self.sendMessage('r' + str(r))
        self.sendMessage('g' + str(g))
        self.sendMessage('b' + str(b))

    def handleClose(self):
        clients.remove(self)
        #print (self.address, 'closed')

server = SimpleWebSocketServer('', 5000, SimpleSliderColor)
print ("Starting to serve on port 5000")
server.serveforever()

