from machine import ADC, Pin, PWM, SoftI2C
import time

# Here we import another library that knows how to draw things on the
# small screen that's included in the kit
import ssd1306

led = PWM(Pin(9))
mic = ADC(Pin(4))

# I2C is a type of protocol. That is, a language that two devices can use
# to communicate with each other. The SoftI2C class allows us to define
# which pins on the microcontroller that we are using and returns an interface
# we can use in code to read and write messages to each device.
i2c_oled = SoftI2C(scl=Pin(7), sda=Pin(6))

# set up the OLED screen with a width of 128 and height of 64 and
# attach it to our I2C pins
oled = ssd1306.SSD1306_I2C(128, 64, i2c_oled)

# The PWM class allows a duty cycle to be set between 0 and 1023.
# The duty cycle means how long is the signal in an on state in
# a given cycle. The higher the number, the brighter the LED will
# appear to be.
CURRENT_BRIGHTNESS = 1023
CANDLE_OUT = 0


def get_avg_mic_volume(samples: int = 100):
    """This function will return an average of the current volume
    the microphone is measuring. We take an average to help eliminate
    noise that the microphone might pick up and smooth out transitions.
    """

    avg_volume = sum([mic.read() for i in range(samples)]) / samples

    # the microphone reports a number between 0-4095 where 0 means
    # the loudest and 4095 meaning the quietest. Let's return a
    # number between 0-1023 instead to match the kind of input our LED wants

    scale_factor = 1024 / 4096
    scaled_value = avg_volume * scale_factor
    return int(scaled_value)


def set_candle_brightness():
    """Set the candle brightness to match how much volume
    the speaker is picking up. If it's more than the current
    brightness, then dim the candle. If it's less, then let
    the candle flame slowly recover.
    """

    global CURRENT_BRIGHTNESS, CANDLE_OUT

    avg_volume = get_avg_mic_volume()
    if avg_volume < CURRENT_BRIGHTNESS:
        CURRENT_BRIGHTNESS = avg_volume
    else:
        CURRENT_BRIGHTNESS += 10
        CURRENT_BRIGHTNESS = min(CURRENT_BRIGHTNESS, 1023)

    led.duty(CURRENT_BRIGHTNESS)

    # if the brightness is low for a while, the candle will
    # go out
    if CURRENT_BRIGHTNESS < 200:
        CANDLE_OUT += 1
        led.duty(0)


def update_screen(candle_level):
    # first, erase the previous contents of the screen (fills all pixels with black)
    oled.fill(0)

    # then write out our strings to the screen buffer
    oled.text("Candle Brightness", 0, 0)
    oled.text(f"{candle_level}", 0, 10)

    # finally, we have to call show so that the screen updates all of the new contents
    oled.show()


while CANDLE_OUT < 50:
    set_candle_brightness()
    update_screen(CURRENT_BRIGHTNESS)
update_screen("Blown Out")
