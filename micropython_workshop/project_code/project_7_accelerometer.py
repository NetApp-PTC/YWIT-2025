"""
This project shows how you can use the input from an accelerometer to make an interactive game. The
code below creates a simple game where a ball moves around the screen in response to tilting the
device. If the ball hits the edge of the screen, the game ends.
"""

from machine import Pin, SoftI2C
import mpu6050
import ssd1306

# Set up our OLED display
i2c_oled = SoftI2C(scl=Pin(7), sda=Pin(6))
screen_size = (128, 64)
oled = ssd1306.SSD1306_I2C(*screen_size, i2c_oled)

# Set up our accelerometer
mpu = mpu6050.MPU6050(SoftI2C(scl=Pin(20), sda=Pin(8)))
mpu.wake()


class Ball:
    """A class representing the moving ball on our game's table.
    It will update itself in response to the accelerometer data changing.
    """

    def __init__(self):
        # start in the middle of the screen
        self.x = screen_size[0] / 2
        self.y = screen_size[1] / 2

    def update(self, accel) -> bool:
        self.x += accel[1]
        self.y += accel[0]

        if self.x <= 0 or self.x >= screen_size[0]:
            return False
        if self.y <= 0 or self.y >= screen_size[1]:
            return False

        return True

    def draw(self):
        oled.pixel(int(self.x), int(self.y), 1)

def end_game():
    oled.fill(0)
    oled.text("Game Over", 30, 30, 1)
    oled.show()

def measure(objects):
    result = True

    # get the current data from the sensor
    accel = mpu.read_accel_data()

    # pass it to each object to update themselves with
    for obj in objects:
        result &= obj.update(accel)

    return result

def draw_screen(objects):
    oled.fill(0)
    oled.rect(0, 0, 128, 64, 1)
    for obj in objects:
        obj.draw()
    oled.show()

def game_loop(objects):
    while True:
        if not measure(objects):
            end_game()
            return
        draw_screen(objects)

# start with just a single ball object
objects = [Ball()]
game_loop(objects)
