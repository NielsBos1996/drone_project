import numpy as np
import json

from typing import List

from src.drone import Drone
from src.space import Space
from src.helpers import *


class Solver:
    def __init__(self, targets_location: str, drone_count: int,
                 min_distance: float = 1, max_time=250):
        self.drones = self.init_drones(drone_count, mock=True)
        self.targets = self.read_target(targets_location, drone_count)

        self.space = Space(max_time, drone_count, min_distance)
        self.targets_count = len(self.targets['targets'])
        self.drone_count = drone_count
        self.max_time = max_time

    @execution_log
    def solve(self):
        start_time = 0
        for i in range(self.targets_count):
            is_last = i == self.targets_count - 1
            self.assign_drone_to_target(i)
            finish_time = self.move_drones_to_target(start_time,
                                                     is_last=is_last)
            finish_time += self.targets['wait'][i] * 10

            if finish_time >= self.max_time:
                return
            start_time = finish_time

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

        # FIXME: mogelijk naar np.max zetten om fout te reproduceren dat
        #  drones in elkaar botsen
        closest_distance = np.min(distance, 1)
        for i in np.argsort(closest_distance):
            distance_drone = distance[i]
            target_idx = np.argmin(distance_drone)
            self.drones[i].set_target(targets[target_idx])
            # set to inf because no other drone may take this target
            distance[:, target_idx] = np.inf

    def move_drones_to_target(self, time, is_last) -> int:
        """Checks if it is possible to move all the drones in a straight
        line to their targets
        Execute the movements if possible
        If not possible, use the move_drones_up_straight algorithm"""
        et = self.move_drones_straight(time)
        if not et:
            return self.move_drones_up_straight(time, is_last)
        return et

    def move_drones_straight(self, time) -> int:
        """tries to move all the drones in a straight line to their targets.
        returns 0 if this is not possible"""
        return 0

    def move_drones_up_straight(self, time, is_last) -> int:
        """This function has a while loop which goes on in the time
        it starts by letting all the drones fly up, and when they reach
        their target height the drones will go in a straight way to their goal
        """
        # TODO: als twee drones continue niet kunnen bewegen omdat ze in
        #  elkaars weg zitten moet dit gespot worden en moet (minstens) een
        #  drone toch bewegen, zodat bijde drones de target kunnen halen
        while True:
            all_drones_finished = True
            for idx, drone in enumerate(self.drones):
                if drone.reached_goal(): continue
                all_drones_finished = False
                td = drone.target_diff()
                mfs = drone.max_flight_speed

                move = self.calculate_move(drone, td, mfs, z_first=not is_last)
                self.move_drone(drone, idx, move, time)

            time += 1
            if time == self.max_time:
                return time

            if all_drones_finished:
                break
        return time

    def calculate_move(self, drone, td, mfs, z_first: bool):
        z_reached = abs(td[2]) < .001
        if z_reached or not z_first:
            # move drone in xy plane
            if np.linalg.norm(td[:2]) <= mfs:
                # drone is within one move of the goal
                move = [td[0], td[1], 0]
            else:
                # drone is more than one move away from goal
                move = list(mfs * td[:2] / np.linalg.norm(td[:2]))
                move.append(0)
        else:
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
                    move = [0, 0, -mfs]

        return move

    def move_drone(self, drone, drone_number, move, time) -> None:
        drone_new_loc = drone.pos_after_move(move)
        conflicting_drone_idx = self.space.set_drone_loc(time, drone_number,
                                                         drone_new_loc)
        if not conflicting_drone_idx:
            drone.update(move)
        else:
            if self.drones[conflicting_drone_idx].reached_goal():
                self.flip_goals(drone_number, conflicting_drone_idx)
            else:
                # for debugging purposes
                write_log(f"drone {drone_number}: {drone.debug_info()}")
                write_log(f"drone {conflicting_drone_idx}: "
                          f"{self.drones[conflicting_drone_idx].debug_info()}")

    def flip_goals(self, drone1, drone2):
        write_log(f"flipping goals drones {drone1} and {drone2}")
        t1 = self.drones[drone1].get_target()
        t2 = self.drones[drone2].get_target()
        self.drones[drone1].set_target(t2)
        self.drones[drone2].set_target(t1)

    def read_target(self, target_file, drone_count):
        """targets should contain
        targets['targets'][target_count][drone_count]
        targets['wait'][target_count']
        """
        with open(target_file, 'r') as file:
            targets = json.load(file)
            end_pos = []
            for idx, drone in enumerate(self.drones):
                end_pos.append(drone.serialize())
            targets["targets"].append(end_pos)
            targets["wait"].append(1)
            pass
        if len(targets['targets']) != len(targets['wait']):
            raise ValueError("targets and wait length do not match")
        if not targets['targets'][0]:
            raise ValueError("no targets in target file")
        if len(targets['targets'][0]) != drone_count:
            raise ValueError("drones count in target and available drones do not match")
        return targets

    @staticmethod
    def init_drones(drone_count: int, mock: bool) -> List[Drone]:
        drones = []
        if mock:
            # for now we lay the drones in a grid on the ground
            x = int(np.ceil(drone_count ** .5))
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
    s = Solver(targets_location="../data/targets/eight_drones.json",
               drone_count=8,
               min_distance=1, max_time=300)
    s.solve()
