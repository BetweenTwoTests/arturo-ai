from graph import Graph
from itertools import product
from collections import defaultdict

# ☐ ══☐   ☐ ══☐ 
# ║   ║   ║   ║ 
# ☐   ☐ ══☐   ☐ 
# ║   ║   ║   ║ 
# ☐ ══☐   ☐ ══☐ 
# ║       ║   ║ 
# ☐   ☐ ══☐   ☐ 
# V1 = list(product(range(4), range(4)))
# E1 = [((0,0), (0,1)), ((0,1), (0,2)),
#       ((0,1), (1,1)), ((0,2), (0,3)),
#       ((0,3), (1,3)), ((1,1), (1,2)),
#       ((1,2), (1,3)), ((1,2), (2,2)),
#       ((2,2), (2,1)), ((2,1), (2,0)),
#       ((2,1), (3,1)), ((2,0), (1,0)),
#       ((2,2), (2,3)), ((2,3), (3,3)),
#       ((3,3), (3,2)), ((3,2), (3,1)),
#       ((3,1), (3,0))]
# grid_1 = Graph(V1, E1)

# Footbal field: 8 x 5
#       ----  ☐ -----
#       ☐══☐══☐══☐══☐
#       ║  ║  ║  ║  ║
#       ☐══☐══☐══☐══☐
#       ║  ║  ║  ║  ║
#       ☐══☐══☐══☐══☐
#       ║  ║  ║  ║  ║
#       ☐══☐══☐══☐══☐
#       ║  ║  ║  ║  ║
#       ☐══☐══☐══☐══☐
#       ║  ║  ║  ║  ║
#       ☐══☐══☐══☐══☐
#       ║  ║  ║  ║  ║
#       ☐══☐══☐══☐══☐
#       ║  ║  ║  ║  ║
# (0,0) ☐══☐══☐══☐══☐
# --- start ---
obstacles = defaultdict(bool)
obstacle_edges = [
    ((0,0), (0,1)),
    ((1,0), (1,1))
]
for edges in obstacle_edges:
    obstacles[edges] = True

football_field = Graph(obstacles)







    


