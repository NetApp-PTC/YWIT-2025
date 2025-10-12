"""
This project code implements a "world's worst piano" using a rotary encoder, an OLED display, and a speaker.
The user can select musical notes using the rotary encoder, add them to a song by pressing the encoder's button,
and play back the composed song through the speaker. The OLED display shows the currently selected note.

It may not be easy to play, but it will make all sort of interesting noises!
"""

from machine import Pin, SoftI2C, PWM
import time

from debounced_button import DebouncedButton
from rotary_irq import RotaryIRQ
import ssd1306


# frequencies of notes (based on A=440Hz)
NOTES = [
    ("A0", 110),
    ("Bb0", 117),
    ("B0", 123),
    ("C0", 131),
    ("C#0", 139),
    ("D0", 147),
    ("Eb0", 156),
    ("E0", 165),
    ("F0", 173),
    ("F#0", 185),
    ("G0", 196),
    ("G#0", 208),
    ("A1", 220),
    ("Bb1", 233),
    ("B1", 247),
    ("C1", 262), # middle C
    ("C#1", 277),
    ("D1", 294),
    ("Eb1", 311),
    ("E1", 330),
    ("F1", 349),
    ("F#1", 370),
    ("G1", 392),
    ("G#1", 415),
    ("A2", 440),
    ("Bb2", 466),
    ("B2", 494),
    ("C2", 523), # C inside the staff
    ("C#2", 554),
    ("D2", 587),
    ("Eb2", 622),
    ("E2", 659),
    ("F2", 698),
    ("F#2", 740),
    ("G2", 784),
    ("G#2", 831),
    ("A3", 880),
    ("Bb3", 932),
    ("B3", 988),
    # Notes above 1KHz won't play correctly on an ESP8266 because it's only capable of 1k maximum
    # for the PWM. If these are attempted, they get clamped to 1k. They will work fine on the ESP32
    # though since it can go up to 40MHz!
    ("C3", 1047), # C above the staff
    ("C#3", 1109),
    ("D3", 1175),
    ("Eb3", 1245),
    ("E3", 1319),
    ("F3", 1397),
    ("F#3", 1480),
    ("G3", 1577),
    ("G#3", 1661),
]
user_song = []


def play_song(_):
    """Play back the song that the user has composed."""

    print("Playing your song...")
    for note in user_song:
        print(f"Playing {note[0]}")
        play_note(NOTES.index(note), duration_ms=300)
        time.sleep_ms(100)
    print("Your song is finished!")


def setup_components():
    """Set up all of our components so that the user can interact with them."""

    global oled, speaker, knob

    # Set up our OLED display
    i2c_oled = SoftI2C(scl=Pin(7), sda=Pin(6))
    oled = ssd1306.SSD1306_I2C(128, 64, i2c_oled)

    # Set up our speaker
    speaker = Pin(20, Pin.OUT)

    # Set up our rotary encoder
    knob = RotaryIRQ(
        pin_num_clk=10, pin_num_dt=9, min_val=0, max_val=len(NOTES)-1,
        reverse=True, range_mode=RotaryIRQ.RANGE_BOUNDED
    )
    knob.add_listener(lambda: update_screen(knob.value()))

    DebouncedButton(8, handle_button)
    DebouncedButton(5, play_song)


def handle_button(_):
    """This function is called whenever the button on the rotary encoder is pressed."""

    value = knob.value()
    user_song.append(NOTES[value])
    print(f"Added {NOTES[value][0]} to your song!")


def update_screen(value):
    """Update the OLED screen to show the currently selected note."""

    # first, erase the previous contents of the screen (fills all pixels with black)
    oled.fill(0)

    # then write out our strings to the screen buffer
    oled.text(f"Note: {NOTES[value][0]}", 0, 0)

    # finally, we have to call show so that the screen updates all of the new contents
    oled.show()


def play_note(value, duration_ms: int = 500):
    """Play a note through our speaker for a given duration in milliseconds."""

    pwm = PWM(speaker, freq=NOTES[value][1], duty=512)
    time.sleep_ms(duration_ms)

    # stops the notes playing
    pwm.deinit()


# set up all of our components so that the user can interact with them
setup_components()
update_screen(0)
