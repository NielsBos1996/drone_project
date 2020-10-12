import numpy as np

class Drone:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.v = 0
        self.phi = 0
        self.theta = 0

    def update(self, x, y, z, v, phi, theta):
        self.x = x
        self.y = y
        self.z = z
        self.v = v
        self.phi = phi
        self.theta = theta

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

