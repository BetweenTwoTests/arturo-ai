from graph import Graph
from itertools import product
from collections import defaultdict

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
obstacles = defaultdict(bool)
obstacle_edges = [
    ((0,0), (0,1)), ((1,0), (1,1)),
    ((1,1), (1,2)), ((2,1), (2,2)), ((3,1), (3,2)), ((4,1), (4,2)),
    ((1,3), (2,3)), ((1,4), (2,4)), ((1,5), (2,5)),
    ((3,5), (4,5)), ((3,6), (4,6)), ((3,7), (4,7))
]
for edges in obstacle_edges:
    obstacles[edges] = True

football_field = Graph(obstacles)



    


