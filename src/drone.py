import numpy as np


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

    def update(self, xyz):
        assert len(xyz) == 3
        self.x += xyz[0]
        self.y += xyz[1]
        self.z += xyz[2]
        return np.array([self.x, self.y, self.z])

    def set_target(self, xyzc: list) -> None:
        assert len(xyzc) == 4
        self.target_x = xyzc[0]
        self.target_y = xyzc[1]
        self.target_z = xyzc[2]
        self.color = xyzc[3]

    def reached_goal(self) -> bool:
        if abs(self.x - self.target_x) > .001:
            return False
        if abs(self.y - self.target_y) > .001:
            return False
        if abs(self.z - self.target_z) > .001:
            return False
        return True

    def target_diff(self):
        return np.array([self.target_x - self.x,
                         self.target_y - self.y,
                         self.target_z - self.z])

    def serialize(self):
        return [self.x, self.y, self.z, f"#{self.color}"]

    @property
    def location(self):
        return np.array([self.x, self.y, self.z])