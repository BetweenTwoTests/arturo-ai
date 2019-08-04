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


class HorizontalBadAgent:
    def __init__(self, droid_name, position, min_bound, max_bound):
        self.position = position
        self.min_bound = min_bound
        self.max_bound = max_bound

        droid_client = DroidClient()
        droid_client.scan()
        droid_client.connect_to_droid(droid_name)
        self.droid_client = droid_client
    
    def move(self):
        x, y = self.position
        direction = 1 if (self.max_bound[1] - y) > 0 else -1
        new_position = (x, y + direction)
        print("move bad bot: {0}".format([self.position, new_position]))
        maneuver.follow_path(
            self.droid_client, 
            [self.position, new_position],
            speed = 0x88)
        self.position = new_position

# get course, find path
G = courses.football_field
G.print()
agent_droid = DroidClient()
agent_droid.scan()
agent_droid.connect_to_droid('Q5-8CC0') # Agent
enemy_droid = HorizontalBadAgent('D2-6F8D', position = (3, 3), 
    min_bound = (3, 1), max_bound = (3, 7))

agent_start = (0, 0)
agent_goal = (4, 7)
while True:
    if(agent_start == agent_goal):
        break
    
    #  AGENT
    path = A_star(G, agent_start, agent_goal)
    path = path[0:2]
    agent_start = path[1]
    print("move: {0}".format(path))
    maneuver.follow_path(agent_droid, path, speed = 0x88, scale_dist = 1)
    
    # BAD DROID 1
    enemy_droid.move()