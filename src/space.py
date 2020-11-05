import numpy as np

from src.helpers import *


class Space:
    def __init__(self, max_time: int, drone_count: int, min_distance: float):
        """drone_loc contains
        the xyz locations of each drone for all the time stemps
        drone_loc[time][drone_number][xyz (012)]
        """
        self.max_time = max_time
        self.min_distance = min_distance
        self.drone_count = drone_count
        self.drone_locs = np.zeros((max_time * 10, drone_count, 3)).astype(
            'float32')

    def set_drone_loc(self, time, drone_number, drone_loc):
        """loc must be a numpy array with 3 elements
        if the drone cannot make a move, the number of the drone which
        is in the way is returned. if it is possible to make the move,
        None is returned"""
        for idx, other_drone_loc in enumerate(self.drone_locs[time, :, :]):
            if idx == drone_number:
                continue
            if drone_loc[2] < 1:
                # dont check distance when close to the ground
                continue

            # check distance between drones
            distance = np.linalg.norm(drone_loc - other_drone_loc)
            if distance < self.min_distance:
                write_log(f"Unable to move drone {drone_number}, drone {idx} is in the way")
                return idx
        self.drone_locs[time:, drone_number, :] = drone_loc
        return None

    def reset(self, time):
        """Sets everything after time to zero"""
        self.drone_locs[time:] = 0

    def __repr__(self):
        return f"Space object with drones={self.drone_count}&timespan={self.max_time}"
