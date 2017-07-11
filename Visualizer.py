import neopixel
import time


class Visualizer(object):
    def __init__(self, numberOfLeds, numberOfBars, x_direction, y_direction):
        self.numberOfLeds = numberOfLeds
        self.pin = 18
        self.frequency = 800000
        self.dma = 5
        self.brightness = 255
        self.invert = False
        self.channel = 0
        self.stripType = neopixel.ws.WS2811_STRIP_GRB
        self.strip = neopixel.Adafruit_NeoPixel(
            self.numberOfLeds,
            self.pin,
            self.frequency,
            self.dma,
            self.invert,
            self.brightness,
            self.channel,
            self.stripType)
        self.strip.begin()
        self.x_flow = x_direction
        self.y_flow = y_direction
        self.visualizerArray = []
        self.numberOfLedsPerBar = int(numberOfLeds / numberOfBars)
        self.numberOfBars = numberOfBars
        self.__initialize_array()

    def __initialize_array(self, color=[0, 0, 0]):
        vertical_bool = int(self.y_flow == 'down')
        for x in range(self.numberOfBars):
            bar = []
            for y in range(self.numberOfLedsPerBar):
                index = (x * 15) + y \
                    if x % 2 == vertical_bool \
                    else (x + 1) * 15 - (y + 1)
                led = [index, color]
                bar.append(led)
            self.visualizerArray.append(bar)
        if self.x_flow != 'right':
            self.visualizerArray.reverse()

    def color_led(self, led, show=True):
        self.strip.setPixelColor(led[0], neopixel.Color(*(led[1])))
        if show: self.strip.show()

    def color_bar(self, bar):
        for led in bar:
            self.color_led(led)
            time.sleep(0.1)

    def wipe(self, color=[0, 0, 0]):
        for x in range(self.numberOfBars):
            for y in range(self.numberOfLedsPerBar):
                self.visualizerArray[x][y][1] = color
        for bar in self.visualizerArray:
            self.color_bar(bar)
