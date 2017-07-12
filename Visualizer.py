import neopixel
import time


class LED(object):
    def __init__(self, index, color):
        self.index = index
        self.color = color

    def get(self, prop='led'):
        if not self.index: return False
        if prop == 'index':
            return self.index
        elif prop == 'color':
            return self.color
        elif prop == 'led':
            return [self.index, self.color]

    def setColor(self, color):
        self.color = color

    def colorLED(self, strip, show=False):
        strip.setPixelColor(self.index, neopixel.Color(*(self.color)))
        if show: strip.show()

    def off(self, strip=None, show=False):
        self.setColor([0, 0, 0])
        if strip != None:
            self.colorLED(strip, show)


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
        self.show = self.strip.show
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
                led = LED(index, color)
                bar.append(led)
            self.visualizerArray.append(bar)
        if self.x_flow != 'right':
            self.visualizerArray.reverse()

    def color_bar(self, bar_position):
        for i in range(self.numberOfLedsPerBar):
            self.visualizerArray[bar_position][i].colorLED(self.strip)
        self.show()

    def color_array(self):
        for bar in self.visualizerArray:
            for led in bar:
                led.colorLED(self.strip)
        self.show()

    def set_bar_percent(self, bar_position, percent, color=[255, 255, 255]):
        if not (0 <= bar_position < self.numberOfBars): return False

        number_of_leds = int(round(percent * self.numberOfLedsPerBar))
        for i in range(number_of_leds):
            self.visualizerArray[bar_position][i].setColor(color)
        for i in range(number_of_leds, self.numberOfLedsPerBar):
            self.visualizerArray[bar_position][i].off()

    def wipe(self, color=[0, 0, 0]):
        for bar in self.visualizerArray:
            for led in bar:
                led.setColor(color)
                led.colorLED(self.strip)
            self.show()


from random import random
import time

v = Visualizer(150, 10, 'left', 'down')
v.wipe()
for i in range(1000):
    for i in range(10):
        red = int(round(random() * 255))
        green = int(round(random() * 255))
        blue = int(round(random() * 255))
        color = [red, green, blue]
        v.set_bar_percent(i, random(), color)
    v.color_array()
    time.sleep(0.04)
