import random
import maneuver

def good_droid_turn(droid, w, G, victory_state, warriors):

    if not (droid.get_is_alive()):
        print("YOU LOST")
        # droid falls over
        return True

    path = A_star(G, droid.get_location(), victory_state)
    path = get_path(droid, path)
    if not path:
        return True # game over

    x, y = path[0]
    # Update grid states
    # Update agent's position
    G.update_agent_position(droid.ID, droid.get_location())
    # Update grid so that old position (x,y) is now available for move into
    # while new position is not available into
    G.update_neighbors((x,y), droid.get_location())
    maneuver.follow_path(droid, path, speed = 0x88, scale_dist = 1)

    if droid in victory_state:
        print("YOU WON")
        # chirping Sound
        agent_droid.animate(5)
        # headspin
    else:
        dist, bad_droid = get_nearest_opponent(droid.get_location(), warriors)
        if 1 < dist < 2:
            bad_droid.set_is_active(False)
            # headspin
    return False

def bad_droid_turn(droid, warriors, G):

    # Skip Droid's Turn
    if not droid.get_is_active():
        droid.set_is_active(True)
        return False

    dist, closest_droid = get_nearest_opponent(droid.get_location(), warriors)
    path = a_star(G, droid.get_location(), closest_droid.get_location())

    path = get_path(droid, path)
    if not path:
        return True # game over
    x, y = path[0]
    # Update grid states
    # Update agent's position
    G.update_agent_position(droid.ID, droid.get_location())
    # Update grid so that old position (x,y) is now available for move into
    # while new position is not available into
    G.update_neighbors((x,y), droid.get_location())
    maneuver.follow_path(droid, path, speed = 0x88, scale_dist = 1)
    
    return False

def launch_EMP(self, bad_guy):
    bad_guy.set_is_active(False)
    # use_weapon("EMP")

def got_speed_boost():
    return (random.random() < 0.2)

def get_nearest_opponent(location, warriors):

    d_min = math.inf
    opponent = None
    for w in warriors:
        if w.get_is_good():
            dist = compute_distance(location, w.get_location())
                if dist < d_min:
                    d_min = dist
                    opponent = w

    return d_min, opponent

def get_path(droid, path):

     if path is None:
        return False

    if got_speed_boost():
        path = path[0:3]
        droid.set_location(path[2])
    else:
        path = path[0:2]
        droid.set_location(path[1])

    return path

def compute_distance(location1, location2):
    x_1, y_1 = location1
    x_2, y_2 = location2
    d_x, d_y = (x_2 - x_1), (y_2 - y_1)
    return math.sqrt(d_x**2 + d_y**2)
