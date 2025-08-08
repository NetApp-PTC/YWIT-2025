from machine import Pin

class SevenSegmentDisplay:
    def __init__(self, pins):
        self.pins = [Pin(pin, Pin.OUT) for pin in pins]
        self.segments = {
            '0': (0, 1, 1, 1, 1, 1, 1),
            '1': (0, 0, 0, 1, 1, 0, 0),
            '2': (1, 0, 1, 1, 0, 1, 1),
            '3': (1, 0, 1, 1, 1, 1, 0),
            '4': (1, 1, 0, 1, 1, 0, 0),
            '5': (1, 1, 1, 0, 1, 1, 0),
            '6': (1, 1, 1, 0, 1, 1, 1),
            '7': (0, 0, 1, 1, 1, 0, 0),
            '8': (1, 1, 1, 1, 1, 1, 1),
            '9': (1, 1, 1, 1, 1, 1, 0)
        }

    def display(self, number):
        number = str(number)
        if number not in self.segments:
            raise ValueError("Number must be between 0 and 9")

        for index, pin in enumerate(self.pins):
            pin.value(self.segments[number][index])

    def clear(self):
        for pin in self.pins:
            pin.value(0)
