import numpy as np

class Drone:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        # velocity / acceleration?
        # angle? (rx ry rz)

    def move(self, x, y, z):
        self.x += x
        self.y += y
        self.z += z

    def update(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


def calc_coords(drones: list, information: list) -> np.ndarray:
    """
    pakt een list met alle drones als input en update de locatie van de drones
    door middel van de update functie
    """


def path_finding(drones: list):
    pass


if __name__ == '__main__':
    drones = [Drone(0,0,0), Drone(1, 0, 0)]

    path_finding(drones)

