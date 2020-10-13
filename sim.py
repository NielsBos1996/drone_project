import io
import os
import subprocess

import imageio
import matplotlib.pyplot as plt
import numpy as np

from drone import Drone
from path_finding import path_finder, set_drone_target, is_done
from helpers import *


class DroneSimulaterPlot:
    def __init__(self):
        self.images = []

    def make_plot(self, drones):
        drone_count = len(drones)
        x = np.zeros((1, drone_count))
        y = np.zeros((1, drone_count))
        z = np.zeros((1, drone_count))
        c = np.zeros((1, drone_count)).astype(str)

        for idx, drone in enumerate(drones):
            x[idx] = drone.x
            y[idx] = drone.y
            z[idx] = drone.z
            c[idx] = drone.color

        buf = io.BytesIO()
        fig = self.scatter(x, y, z, c, xmin=0, xmax=10, ymin=0, ymax=10,
                           zmin=0,
                           zmax=10, title=f'frame: {len(self.images)}')
        fig.savefig(buf, format='png')
        self.images.append(buf)
        plt.close()

    @staticmethod
    def scatter(x, y, z, c, xmin=None, xmax=None, ymin=None, ymax=None,
                zmin=None,
                zmax=None, title=""):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(x, y, z, c)
        if xmin is not None and xmax is not None:
            ax.set_xlim(xmin, xmax)
        if ymin is not None and ymax is not None:
            ax.set_ylim(ymin, ymax)
        if zmin is not None and zmax is not None:
            ax.set_zlim(zmin, zmax)
        if title:
            ax.set_title(title)
        return fig

    def make_gif(self, name: str, show=True):
        if not name.endswith('.gif'):
            name += '.gif'
        with imageio.get_writer(name, mode='I') as writer:
            for path_to_image in self.images:
                path_to_image.seek(0)
                img = imageio.imread(path_to_image)
                writer.append_data(img)
        if show:
            subprocess.check_output([f'{os.getcwd()}\\{name}'], shell=True)


def update_drones(drones, target_time):
    # TODO
    pass


def simulation_single_drone_up():
    drones = [Drone(1, 2, 3, "b")]
    simulator = DroneSimulaterPlot()
    for time in range(1, 100):
        drones[0].z += 0.1
        simulator.make_plot(drones)
    simulator.make_gif(name='test')


def simulation_pathinding_algorithm():
    drones = []
    drones.append(Drone(4, 3, 0, 'red'))
    drones.append(Drone(8, 3, 0, 'green'))
    drones.append(Drone(4, -3, 0, 'blue'))
    drones.append(Drone(8, -3, 0, 'orange'))

    target = {
        "time": 1.234,
        "locations": [
            [1, 1, 1],
            [1, 0, 1],
            [0, 1, 1],
            [0, 0, 1]
        ]
    }

    simulator = DroneSimulaterPlot()

    set_drone_target(drones, target)

    while not is_done(drones):
        simulator.make_plot(drones)
        path_finder(drones)
        update_drones(drones, 1)
    simulator.make_plot(drones)
    simulator.make_gif("done_simulatie")
