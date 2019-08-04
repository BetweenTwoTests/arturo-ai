# agent_droid = DroidClient()
# agent_droid.scan()
# agent_droid.connect_to_droid('Q5-8CC0') # Agent

# enemy_droid = DroidClient()
# enemy_droid.scan()
# enemy_droid.connect_to_droid('D2-6F8D') # Agent

# for i in range(3):
#     maneuver.follow_path(agent_droid, [(0,0), (0,1), (0,2), (0,3), (0,4), (0,5), (0,6)], speed = 0x88)
#     maneuver.follow_path(enemy_droid, [(0,0), (0,1), (0,2), (0,3), (0,4), (0,5), (0,6)], speed = 0x88)


import sys
import time
from client import DroidClient
import courses
from a_star import A_star
import maneuver


class BadAgent:
    def __init__(self, droid_name, direction, position, min_bound, max_bound):
        self.position = position
        self.direction = direction
        self.min_bound = min_bound
        self.max_bound = max_bound
        droid_client = DroidClient()
        droid_client.scan()
        droid_client.connect_to_droid(droid_name)
        self.droid_client = droid_client
    
    def move(self):
        x, y = self.position

        if self.direction == "horizontal":
            direction = 1 if (self.max_bound[0] - self.min_bound[0] - x) > 0 else -1
        elif self.direction == "vertical":
            direction = 1 if (self.max_bound[1] - self.min_bound[1] - y) > 0 else -1
        elif self.direction == "random":
            # move randomly within the square drawn by (min_bound, max_bound)
            # make sure to check for obstacles
            pass
        else:
            raise Exception("Bad Agent move direction is badly specified")
        new_position = (x + direction, y)
        maneuver.follow_path(
            self.droid_client, 
            [self.position, new_position],
            speed = 0x88)
        self.position = new_position
        print("move bad bot: {0}".format([self.position, new_position]))


good_agent = "Q5-8CC0"
bad_agents = ["D2-6F8D", "D2-4D79"]
G = courses.football_field
G.agent_positions = {
    good_agent : (0,0),
    bad_agents[0] : (1,6),
    bad_agents[1] : (0,3)
}
G.print()

good_droid = DroidClient()
good_droid.scan()
good_droid.connect_to_droid('Q5-8CC0') # Agent
goal = (4, 7)

# Enemy droids
enemy_droid_horizontal = BadAgent(bad_agents[0], 
    direction = "horizontal", 
    position = (1, 6),
    min_bound = (1, 6), max_bound = (3, 6))

enemy_droid_vertical = BadAgent(bad_agents[1], 
    direction = "vertical", 
    position = (0, 3),
    min_bound = (0, 3), max_bound = (0, 7))

while True:
    if(G.agent_positions[good_agent] == goal):
        break

    # Print current game state
    print("#" * G.col * 8)
    G.print()
    print("#" * G.col * 8)
    #  AGENT
    path = A_star(G, G.get_position(good_agent), goal)
    path = path[0:2]
    agent_start = path[1]
    print("move: {0}".format(path))
    # maneuver.follow_path(agent_droid, path, speed = 0x88, scale_dist = 1)
    
    # BAD AGENTS
    enemy_droid_horizontal.move()
    enemy_droid_vertical.move()