import numpy as np

from src.helpers import *

class Drone:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.v = 0
        self.color = "000000"
        self.target_x = None
        self.target_y = None
        self.target_z = None

        # can fly up to 3m/second which translates to .3m per .1 second
        # note that a big limitation is that the mock assumes that the drone
        # can go from idle to moving 30 cm within 0.1 second.
        self.max_flight_speed = .1

    def update(self, xyz) -> None:
        assert len(xyz) == 3
        self.x += xyz[0]
        self.y += xyz[1]
        self.z += xyz[2]

    def set_pos(self, xyz) -> None:
        assert len(xyz) == 3
        self.x = xyz[0]
        self.y = xyz[1]
        self.z = xyz[2]

    def pos_after_move(self, xyz) -> np.ndarray:
        """Returns the position of a drone if after it made a given move,
        it doesnt make the move
        """
        assert len(xyz) == 3
        return np.array([self.x+xyz[0], self.y+xyz[1], self.z+xyz[2]])

    def set_target(self, xyzc: list) -> None:
        assert len(xyzc) == 4
        self.target_x = xyzc[0]
        self.target_y = xyzc[1]
        self.target_z = xyzc[2]
        self.color = xyzc[3]

    def get_target(self) -> list:
        return [self.target_x, self.target_y, self.target_z, self.color]

    def reached_goal(self) -> bool:
        if abs(self.x - self.target_x) > .001:
            return False
        if abs(self.y - self.target_y) > .001:
            return False
        if abs(self.z - self.target_z) > .001:
            return False
        return True

    def target_diff(self) -> np.ndarray:
        return np.array([self.target_x - self.x,
                         self.target_y - self.y,
                         self.target_z - self.z])

    def serialize(self) -> list:
        return [self.x, self.y, self.z, f"#{self.color}"]

    def debug_info(self) -> str:
        return f"pos: {self.x:.2f} {self.y:.2f} {self.z:.2f} target: " \
               f"{self.target_x:.2f} {self.target_y:.2f} {self.target_z:.2f}"

    @property
    def location(self) -> np.ndarray:
        return np.array([self.x, self.y, self.z])
