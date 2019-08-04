from collections import defaultdict
from itertools import product
from collections import defaultdict

class Graph:
    def is_obstacle(self, u, v):
        return self.obstacles[(u[0], u[1]), (v[0], v[1])] or \
                self.obstacles[(v[0], v[1]), (u[0], u[1])] 


    def __init__(self, obstacles, agent_positions = {}):
        self.row = 8# 8
        self.col = 5# 5
        self.obstacles = obstacles
        self.V = list(product(range(self.row), range(self.col)))
        self.agent_positions = agent_positions
        self.agent_names = agent_positions.keys()

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
                        not self.is_obstacle((u_x, u_y), (v_x, v_y)) ):
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

    def neighbors(self, u):
        return self.neighborhood[u]

    def update(self, new_obstacles, free_edges):
        # add new obstacles
        for (u, v) in new_obstacles.keys():
            self.neighborhood[u].remove(v)
            self.neighborhood[v].remove(u)

        # delete old obstacles and recover as new_edge
        for (u, v) in free_edges.keys():
            self.neighborhood[u].add(v)
            self.neighborhood[v].add(u)


    def dist_between(self, u, v):
        if v not in self.neighbors(u):
            return None
        return 1 # assumes unweighted graph

    def move_enemy(self, pos, bound):
        n = self.neighborhood[pos]

        for new_pos in n:
            if new_pos[1] <= bound[1] and new_pos[1] >= bound[0]:
                return new_pos

    def print(self):
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
                for valid_neighbor in self.neighbors((x,y)):
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
