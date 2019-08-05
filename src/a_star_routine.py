import sys
import time
from graph import Graph
from collections import defaultdict

# Custom Imports
from Warrior import Warrior

# -- Initialize game
# Footbal field: 8 x 5
#
# Each box is a vertex
#
#       ------ ☐ ------
#       ☐══☐══☐══☐══☐══☐
#       ║           ║  ║
#       ☐  ☐  ☐  ☐  ☐  ☐
#       ║           ║  ║
#       ☐  ☐  ☐  ☐  ☐  ☐
#       ║     ║     ║  ║
#       ☐  ☐  ☐  ☐  ☐  ☐
#       ║     ║        ║
#       ☐  ☐  ☐  ☐  ☐  ☐
#       ║     ║        ║
#       ☐  ☐  ☐  ☐  ☐  ☐
#       ║              ║
#       ☐  ☐══☐══☐══☐══☐
#       ║              ║
#       ☐══☐══☐  ☐  ☐  ☐
#       ║
# (0,0) ☐══☐══☐══☐══☐══☐
# --- start ---

game_over = False

## Graph Construction
obstacles = defaultdict(bool)
obstacle_edges = [
    ((0,0), (0,1)), ((1,0), (1,1)),
    ((1,1), (1,2)), ((2,1), (2,2)), ((3,1), (3,2)), ((4,1), (4,2)),
    ((1,3), (2,3)), ((1,4), (2,4)), ((1,5), (2,5)),
    ((3,5), (4,5)), ((3,6), (4,6)), ((3,7), (4,7))
]
for edges in obstacle_edges:
    obstacles[edges] = True

## Set Up Agents

good_agent = ["D2-0709"]
bad_agents = ["D2-4D79", "D2-6F8D"]

good_agent1 = Warrior("D2-0709", (0, 0), True)
# good_agent2 = Warrior('Q5-8CC0', (0, 4), True)

bad_agent1 = Warrior("D2-4D79", (6, 0), False)
bad_agent2 = Warrior("D2-6F8D", (6, 4), False)


G = Graph(
    obstacles = obstacles,
    agent_positions = {
        good_agents[0] : (0,0),
        # good_agents[1]: (0,4),
        bad_agents[0] : (1,6), # horizontal
        bad_agents[1] : (0,3)  # veritcal
    },
    debug=False
)

goal = (4, 7)

print("Game start!")
G.print()

while True:

    for warrior in warriors:
        if game_over:
            print("----- ENDING GAME -------")
            return

        if warrior.get_is_good():
            game_over = good_droid_turn(warrior, G, goal, warriors)
        else:
            game_over = bad_droid_turn(warrior, warriors)
