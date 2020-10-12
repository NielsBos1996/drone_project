import numpy as np


def set_drone_target(drones, target):
    pass


def path_finder(drones):
    """Steps:
    1) find a direction for the drone with the largest distance to the target
       [x_target, y_target, z_target, time_target]
       the drone goes in a straight line to these coordinates. it will wait
       for the next instruncion upon ariving
    2) repeat till done

    """
    path = []
    pass


def test():
    target = {
        "time": 1.234,
        "locations": [
            [1, 1, 1],
            [1, 0, 1],
            [0, 1, 1],
            [0, 0, 1]
        ]
    }


test()
