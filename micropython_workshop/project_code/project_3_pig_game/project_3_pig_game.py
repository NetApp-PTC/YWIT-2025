import random
import time

from debounced_button import DebouncedButton
from seven_segment import SevenSegmentDisplay

WIN_LIMIT = 100
CURRENT_PLAYER = 2
SCORES = {1: 0, 2: 0}
CURRENT_PLAYER_HELD = 0

def game_win():
    roll_button.disable()
    next_player_button.disable()
    print("---")
    for player, score in SCORES.items():
        print(f"Player {player}: {score} points")
    print(f"Player {CURRENT_PLAYER} wins!")

def roll(_):
    global CURRENT_PLAYER_HELD

    # display a bunch of numbers very fast to mimic
    # rolling a die or spinning a wheel, etc.
    for _ in range(random.randint(40, 100)):
        display.display(random.randint(1, 9))
        time.sleep_ms(15)
    for pause in range(10, 400, 50):
        value = random.randint(1, 9)
        display.display(value)
        time.sleep_ms(pause)

    if value == 1:
        print(f"Oh no! {CURRENT_PLAYER_HELD} points forfeited")
        for _ in range(3):
            display.clear()
            time.sleep_ms(500)
            display.display(value)
            time.sleep_ms(500)
        CURRENT_PLAYER_HELD = 0
        return next_player(None)

    # the last number shown is what we add to the score
    CURRENT_PLAYER_HELD += value
    print(f"Current held points: {CURRENT_PLAYER_HELD}")

def next_player(_):
    global CURRENT_PLAYER, CURRENT_PLAYER_HELD

    # store any accumulated points to the current player
    SCORES[CURRENT_PLAYER] += CURRENT_PLAYER_HELD

    # check if that was enough to win
    if SCORES[CURRENT_PLAYER] >= WIN_LIMIT:
        return game_win()

    # if not report current player score and switch to the next player
    print(f"Player {CURRENT_PLAYER}'s total: {SCORES[CURRENT_PLAYER]}")
    CURRENT_PLAYER_HELD = 0
    CURRENT_PLAYER = 1 if CURRENT_PLAYER == 2 else 2
    print("---")
    print(f"Player {CURRENT_PLAYER}'s turn - You have {SCORES[CURRENT_PLAYER]} points so far")


display = SevenSegmentDisplay([10, 9, 8, 7, 6, 5, 4])
roll_button = DebouncedButton(3, roll)
next_player_button = DebouncedButton(2, next_player)

# start the game
display.clear()
next_player(None)
