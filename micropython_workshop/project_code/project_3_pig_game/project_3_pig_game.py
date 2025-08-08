import random

from debounced_button import DebouncedButton
from seven_segment import SevenSegmentDisplay


def roll(_):
    print("rolling the die")
    display.show(random.randint(0, 9))


def next_player(_):
    print("passing to the next player")


display = SevenSegmentDisplay([8, 20, 21, 7, 6, 5, 4])
roll_button = DebouncedButton(3, roll)
next_player_button = DebouncedButton(2, next_player)
