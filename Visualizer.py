import neopixel


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
        self.__initializeArray()

    def __initializeArray(self):
        verticalBool = int(self.y_flow == 'down') if self.x_flow == 'right' else int(self.y_flow != 'down')
        for x in range(self.numberOfBars):
            bar = []
            for y in range(self.numberOfLedsPerBar):
                index = (x * 15) + y if x % 2 == 0 else (x + 1) * 15 - (y + 1)
                led = (index, (0, 0, 0))
                bar.append(led)
            self.visualizerArray.append(bar)
        if self.x_flow != 'right':
            self.visualizerArray.reverse()

    def colorLed(self, led, show=True):
        self.strip.setPixelColor(led[0], neopixel.Color(*(led[1])))
        if show: self.strip.show()
