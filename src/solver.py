import numpy as np
import json

from typing import List

from src.drone import Drone
from src.space import Space
from src.helpers import *


class Solver:
    def __init__(self, target_file:str, drone_count:int,
                 min_distance:float=1, max_time=70):
        self.targets = self.read_target(target_file, drone_count)
        self.drones = self.init_drones(drone_count, mock=True)
        self.space = Space(max_time, drone_count, min_distance)
        self.targets_count = len(self.targets['targets'])
        self.drone_count = drone_count
        self.max_time = max_time

    def solve(self):
        time = 0
        for i in range(self.targets_count):
            self.assign_drone_to_target(i)
            time = self.up_to_goal(time)
            if time == self.max_time:
                return
            # TODO: drones must sleep like in target file

    def assign_drone_to_target(self, target_number):
        """this function assigns all the drones a target.
        it also checks if it is possible to go straight up and move in a
        straight line to the target. This function SHOULD only give a
        solution when this is the case"""
        targets = self.targets['targets'][target_number]
        distance = np.empty((len(self.drones), len(self.drones)))
        for i, drone in enumerate(self.drones):
            for j, target in enumerate(targets):
                distance[i, j] = np.linalg.norm(drone.location - target[:-1])

        closest_distance = np.min(distance, 1)
        for i in np.argsort(closest_distance):
            distance_drone = distance[i]
            target_idx = np.argmin(distance_drone)
            self.drones[i].set_target(targets[target_idx])
            # set to inf because no other drone may take this target
            distance[:, target_idx] = np.inf


    def up_to_goal(self, time) -> int:
        """This function has a while loop which goes on in the time
        it starts by letting all the drones fly up, and when they reach
        their target height the drones will go in a straight way to their goal
        """
        while True:
            all_drones_finished = True
            for idx, drone in enumerate(self.drones):
                if drone.reached_goal(): continue
                all_drones_finished = False

                td  = drone.target_diff()
                dl = drone.location
                mfs = drone.max_flight_speed
                if abs(drone.z - drone.target_z) > .001:
                    # drone is not on the right height yet
                    if abs(td[2]) < mfs:
                        # drone is within one move from target height
                        move = [0, 0, td[2]]
                    else:
                        # drone is more than one move away from target
                        if drone.z < drone.target_z:
                            # drone is lower then target
                            move = [0, 0, mfs]
                        else:
                            # drone is above target
                            move = [0, 0, mfs]
                else:
                    # drone has reached target height
                    if np.linalg.norm(dl[:2] - td[:2]) <= mfs:
                        # drone is within one move of the goal
                        move = [td[0], td[1], 0]
                    else:
                        # drone is more than one move away from goal
                        move = list(mfs*td[:2]/np.linalg.norm(td[:2]))
                        move.append(0)

                self.move_drone(drone, idx, move, time)
            time += 1
            if time == self.max_time:
                return time

            if all_drones_finished:
                break
        return time

    def move_drone(self, drone, drone_number, move, time) -> None:
        # TODO: is a move is not allowed, then wait till the move is allowed
        drone_loc = drone.update(move)
        if not self.space.set_drone_loc(time, drone_number, drone_loc):
            raise ValueError("move not allowed")

    @staticmethod
    def read_target(target_file, drone_count):
        """targets should contain
        targets['targets'][target_count][drone_count]
        targets['wait'][target_count'
        """
        with open(target_file, 'r') as file:
            targets = json.load(file)
            pass
        if len(targets['targets']) != len(targets['wait']):
            raise ValueError("targets and wait length do not match")
        if not targets['targets'][0]:
            raise ValueError("no targets in target file")
        if len(targets['targets'][0]) != drone_count:
            raise ValueError("drones count in target and available drones do not match")
        return targets

    @staticmethod
    def init_drones(drone_count:int, mock:bool) -> List[Drone]:
        drones = []
        if mock:
            # for now we lay the drones in a grid on the ground
            x = int(np.ceil(drone_count**.5))
            drones_placed = 0
            for i in range(x):
                for j in range(x):
                    drones.append(Drone(i, j, 0))
                    drones_placed += 1
                    if drones_placed == drone_count:
                        return drones
        else:
            raise NotImplementedError


if __name__ == "__main__":
    s=Solver("../data/targets/two_drones.json", drone_count=2, min_distance=1)
    s.solve()