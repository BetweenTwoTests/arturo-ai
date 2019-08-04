from itertools import product
from collections import defaultdict
from client import DroidClient
import math

class Graph:
    def __init__(self, obstacles, agent_positions = {}, row = 8, col = 5):
        self.row = row
        self.col = col
        self.obstacles = obstacles
        self.V = list(product(range(self.row), range(self.col)))

        # list of agent names
        self.agent_names = agent_positions.keys()
        
        # dictionary of { droid_name : (vertex x, vertex y) }
        self.agent_positions = agent_positions

        # dictionaryu of { droid_name : DroidClient }
        self.agent_droidclient = dict()

        # Connect to Droids
        for name in self.agent_names:
            droid_client = DroidClient()
            droid_client.scan()
            droid_client.connect_to_droid(name)
            self.agent_droidclient[name] = droid_client

        # Create grid
        offsets = ((1,0), (0,1), (-1, 0), (0, -1))
        E = []
        for u_x in range(self.col):
            for u_y in range(self.row):
                # print("--{0}".format((u_x, u_y)))
                for offset_row, offset_col in offsets:
                    v_x, v_y = (u_x + offset_row, u_y + offset_col)

                    # print(((u_x, u_y), (v_x, v_y)), end="")
                    if (0 <= u_x < self.col and 0 <= u_y < self.row and 
                        0 <= v_x < self.col and 0 <= v_y < self.row and  
                        not self.is_edge_blocked((u_x, u_y), (v_x, v_y)) ):
                        E.append(
                            ((u_x, u_y), (v_x, v_y))
                        )
                        # print("Edge")
                    # else:
                    #     print("obstacle")

        neighborhood = defaultdict(set)
        for (u,v) in E:
            neighborhood[u].add(v)
            neighborhood[v].add(u) # assumes undirected graph
        self.neighborhood = neighborhood

    # Agent methods
    def get_agents(self):
        """Return all agent by name"""
        return self.agent_names

    def get_agent_position(self, agent_name):
        """Return the agent's position by name"""
        return self.agent_positions[agent_name]

    def get_agent_droidclient(self, agent_name):
        """Return droid client for the agent"""
        return self.agent_droidclient[agent_name]

    def update_agent_position(self, agent_name, new_pos):
        self.agent_positions[agent_name] = new_pos
        return None

    # Grid State methods
    def is_edge_blocked(self, u, v):
        """
        Returns true if the edge between vertices u and v is
        blocked. Edge blocked status is bi-drectional.
        No agent should be able to cross if the edge
        is blocked from both directions u -> v and v -> u.    
        """
        return self.obstacles[(u[0], u[1]), (v[0], v[1])] or \
                self.obstacles[(v[0], v[1]), (u[0], u[1])] 

    def get_neighbors(self, u):
        """
        Return set of vertices ((x1,y1), (x2,y2), ...)
        that any agent can travel to from u
        """
        return self.neighborhood[u]

    def update_neighbors(self, v_to_free, v_to_block):
        """Block & unblock the specified edges bewteen verticies.
        v_to_free: *allow* all of it's *current* neighbors to v
        v_to_bloc: *block* all of it's *current* neighbors to v
        """
        # TODO:
        # delete old obstacles and recover as new_edge
        for neighbor in self.get_neighbors(v_to_free).keys():
            self.neighborhood[neighbor].add(v_to_free)
            self.neighborhood[v_to_free].add(neighbor)

        # add new obstacles
        for neighbor in self.get_neighbors(v_to_block).keys():
            self.neighborhood[neighbor].remove(v_to_block)
            self.neighborhood[v_to_block].remove(neighbor)


    def dist_between(self, u, v):
        """Distance between vertices."""
        if v not in self.get_neighbors(u):
            return None
        return 1 # assumes unweighted graph

    def move_agent(self, agent_name, direction, min_bound, max_bound):
        """Move agent_name"""
        x, y = self.get_agent_position(agent_name)
        direction_x, direction_y = 0, 0
        if direction == "horizontal":
            direction_x = 1 if (max_bound[0] - min_bound[0] - x) > 0 else -1
        elif direction == "vertical":
            direction_y = 1 if (max_bound[1] - min_bound[1] - y) > 0 else -1
        elif direction == "random":
            # TODO
            # move randomly within the square drawn by (min_bound, max_bound)
            # make sure to check for obstacles
            raise Exception("Not yet implemented")
            # direction_x = ...
            # direction_y = ...
        else:
            raise Exception("Bad Agent move direction is badly specified")
        
        new_x, new_y = (x + direction_x, y + direction_y)
        
        # Update grid states
        # Update agent's position
        self.update_agent_position(agent_name, (new_x, new_y))
        
        # Update grid so that old position is now available for move
        # while new position is not available
        self.update_neighbors

        # Physically move robot
        self.follow_path(
            droid_client = self.get_agent_droidclient(agent_name),
            path = [(x,y), (new_x, new_y)]
        )

    def print(self):
        """Print game grid to terminal. For debugging / terminal game play"""
        position_agent = {position: agent for agent, position in self.agent_positions.items()}

        neighbor_width = "        "
        obstacle_width = " ------ "
        bottom = [obstacle_width] * self.col
        print(" " + "".join(bottom))
        for y in range(self.row-1, -1, -1):
            bottom = []
            for x in range(self.col):
                cell = str((x,y)) #+ " " # extra space to line up with droid name
                if (x,y) in position_agent:
                    cell = position_agent[(x,y)]
                    cell = cell.replace("-", "")
                 
                bottom_border = obstacle_width
                left_border = "|" + (" " if x == 0 else "")
                right_border = (" " if x == (self.col - 1) else "") + "|"
                for valid_neighbor in self.get_neighbors((x,y)):
                    if (valid_neighbor[0] == (x - 1)):
                        left_border = " "
                    elif (valid_neighbor[0] == (x + 1)):
                        right_border = " "
                    elif (not y == 0 and valid_neighbor[1] == (y - 1)):
                        bottom_border = neighbor_width
                bottom.append(bottom_border)
                print("{0}{1}{2}".format(
                    left_border, cell, right_border
                ), end = "")       
            print("")
            print("|" + "".join(bottom) + "|")

    # -----------------------------------------
    # Following are copied from maneuver.py
    def follow_path(self, droid_client, path):
        """Helper function to move droid client via vertex path specified.
         Return True if succssful, False otherwise.
        """
        speed, scale_dist = 0x88, 1
        cur_pos = path[0]
        for next_pos in path[1:]:

            # compute distance and angle to next position
            # print('%s -> %s' % (cur_pos, next_pos))
            dist, ang = self.__compute_roll_parameters(cur_pos, next_pos)
            rolled = self.__roll(droid_client, speed, ang, dist*scale_dist)
            if not rolled:
                print('Something went wrong.')
                return False

            cur_pos = next_pos
        # print('Path complete.')
        return True

    def __roll(self, droid_client, speed, ang, time):
        """Helper function to move droid. Use follow_path() instead."""
        return droid_client.roll(speed, ang, time)

    def __compute_roll_parameters(self, old_pos, new_pos):
        """Helper function to move droid. Use follow_path() instead."""
        x_1, y_1 = old_pos
        x_2, y_2 = new_pos
        d_x, d_y = (x_2 - x_1), (y_2 - y_1)

        dist = math.sqrt(d_x**2 + d_y**2)
        ang = 90 - math.atan2(d_y, d_x) * (180/math.pi)

        return dist, ang
