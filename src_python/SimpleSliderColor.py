from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
import sys
import RPi.GPIO as GPIO

# Import the WS2801 module.
import Adafruit_WS2801
import Adafruit_GPIO.SPI as SPI


# Configure the count of pixels:
PIXEL_COUNT = 93

# Alternatively specify a hardware SPI connection on /dev/spidev0.0:
SPI_PORT   = 0
SPI_DEVICE = 0
pixels = Adafruit_WS2801.WS2801Pixels(PIXEL_COUNT, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE), gpio=GPIO)

clients = []
class SimpleSliderColor(WebSocket):
    def handleMessage(self):
        print('handling message ' + self.data)
       	base_g, base_b, base_r = pixels.get_pixel_rgb(0)
        print('got values ', base_r, base_g, base_b)
        col = self.data[0]
        val = int(self.data[1:])
        if col == "r":
            base_r = val
        elif col == "g":
            base_g = val
        elif col == "b":
            base_b = val
        print('changing to ', base_r, base_g, base_b)
        for n in range(PIXEL_COUNT):
            pixels.set_pixel_rgb(n, base_g, base_b, base_r)
        pixels.show()
        for client in clients:
            if client != self:
                client.sendMessage(self.data)

    def handleConnected(self):
        print (self.address, 'connected')
        clients.append(self)

    def handleClose(self):
        clients.remove(self)
        print (self.address, 'closed')

server = SimpleWebSocketServer('', 5000, SimpleSliderColor)
print ("Starting to serve on port 5000")
server.serveforever()

