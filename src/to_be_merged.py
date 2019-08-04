import sys
import time
import random

from client import DroidClient
import courses
from a_star import A_star
import maneuver
import warriors

game_over = False


# get course, find path
G = courses.football_field

victory_state = (7, 2)

good_droid1 = Warrior('Q5-8CC0', (0, 0), True)
good_droid2 = Warrior('Q5-8CC0', (0, 4), True)

bad_droid1 = Warrior('D2-0709', (6, 0), False)
bad_droid2 = Warrior('Q5-8CC0', (6, 4), False)

warriors = [good_droid1, good_droid2, bad_droid1, bad_droid2]

# enemy_droid = HorizontalBadAgent('D2-0709', position = (3, 3),
#     min_bound = (0, 3), max_bound = (3, 3))

agent_goal = (0, 7)

while not game_over:

    for warrior in warriors:
        if warrior.get_is_good():
            good_droid_turn(warrior, G, victory_state, warriors)
        else:
            bad_droid_turn(warrior, warriors)
