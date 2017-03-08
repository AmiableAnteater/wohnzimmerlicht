import sys
import RPi.GPIO as GPIO

# Import the WS2801 module.
import Adafruit_WS2801
import Adafruit_GPIO.SPI as SPI

PIXEL_COUNT = 93


class WS2801Wrapper (Adafruit_WS2801.WS2801Pixels):
    def __init__(self, count, clk=None, do=None, spi=None, gpio=None):
        Adafruit_WS2801.WS2801Pixels.__init__(self, count, clk, do, spi, gpio)

    def __init__(self):
        Adafruit_WS2801.WS2801Pixels.__init__(self, PIXEL_COUNT, spi=SPI.SpiDev(0, 0), gpio=GPIO)

    def set_pixel_rgb(self, n, r, g, b):
        """Set the specified pixel n to the provided 8-bit red, green, blue
        component values.  Note you MUST call show() after setting pixels to
        see the LEDs change color!
        """
        assert 0 <= n < self._count, 'Pixel n outside the count of pixels!'
        self._pixels[n*3] = g & 0xFF
        self._pixels[n*3+1] = b & 0xFF
        self._pixels[n*3+2] = r & 0xFF

    def set_pixels_rgb(self, r, g, b, pixel_iteratable=None):
        """Set the specified pixels in pixel_iteratable to the provided 8-bit red, 
        green, blue component values.  Note you MUST call show() after setting pixels to
        see the LEDs change color!
        """
        if not pixel_iteratable:
            pixel_iteratable = range(self.count())
        for n in pixel_iteratable:
            self.set_pixel_rgb(n, r, g, b)
        
    def get_pixel_rgb(self, n):
        """Retrieve the 8-bit red, green, blue component color values of the
        specified pixel n.  Will return a 3-tuple of red, green, blue data.
        """
        assert 0 <= n < self._count, 'Pixel ' + str(n) + ' outside the count of pixels (' + str(self._count) + ')!'
        return self._pixels[n*3+2], self._pixels[n*3], self._pixels[n*3+1]

    def add_rgb(self, n, r, g, b):
        base_b, base_g, base_r = self.get_pixel_rgb(n)
        self.set_pixel_rgb(n, min(255, r + base_r), min(255, g + base_g), min(255, b + base_b))

    def add_fractional_rgb(self, left_pixel, right_fraction, r, g, b):
        right_r = round(right_fraction * r)
        right_g = round(right_fraction * g)
        right_b = round(right_fraction * b)
        left_r = r - right_r
        left_g = g - right_g
        left_b = b - right_b
        self.add_rgb(left_pixel, left_r, left_g, left_b)
        self.add_rgb(left_pixel + 1, right_r, right_g, right_b)
        
    @staticmethod
    def color_wheel_to_rgb(color_index):
        if color_index < 85:
            return color_index * 3, 255 - color_index * 3, 0
        elif color_index < 170:
            color_index -= 85
            return 255 - color_index * 3, 0, color_index * 3
        else:
            color_index -= 170
            return 0, color_index * 3, 255 - color_index * 3
    
    def set_pixel_colorwheel(self, color_index, pixel_index):
        r, g, b = self.color_wheel_to_rgb(color_index)
        self.set_pixel_rgb(pixel_index, r, g, b)

    def set_pixels_colorwheel(self, color_index, pixel_indices=None):
        r, g, b = self.color_wheel_to_rgb(color_index)
        self.set_pixels_rgb(r, g, b, pixel_indices)


if __name__ == "__main__":
    pixels = WS2801Wrapper()
    # Clear all the pixels to turn them off.
    pixels.clear()
    pixels.show()  # Make sure to call show() after changing any pixels!

    for i in range(pixels.count()):
        r = int(sys.argv[1]) & 0xFF
        g = int(sys.argv[2]) & 0xFF
        b = int(sys.argv[3]) & 0xFF
        pixels.set_pixel_rgb(i, r, g, b)
    pixels.show()

