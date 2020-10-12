import matplotlib.pyplot as plt
import numpy as np
import subprocess
import functools
import tempfile
import imageio
import drone
import time
import io
import os

def write_log(message: str):
    assert isinstance(message, str)
    tempdir = f'{tempfile.gettempdir()}\\drone_project'
    if not os.path.isdir(f'{tempdir}'):
        os.mkdir(f'{tempdir}')
    with open(f'{tempdir}\\log.txt', 'a') as f:
        f.write(f'[{time.time()}] ' + message + '\n')


def execution_log(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        write_log(f'{func.__name__} called')
        st = time.time()
        result = func(*args, **kwargs)
        write_log(f'{func.__name__} finished, execution time={time.time()-st} '
                  f'seconds')
        return result
    return wrapper

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
        fig = self.scatter(x, y, z, c,  xmin=0, xmax=10, ymin=0, ymax=10, zmin=0,
            zmax=10, title=f'frame: {len(self.images)}')
        fig.savefig(buf, format='png')
        self.images.append(buf)
        plt.close()

    @staticmethod
    def scatter(x, y, z, c, xmin=None, xmax=None, ymin=None, ymax=None, zmin=None,
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


def simulation():
    drones = [drone.Drone(1, 2, 3, "b")]
    simulator = DroneSimulaterPlot()
    for time in range(1, 100):
        drones[0].z += 0.1
        simulator.make_plot(drones)
    simulator.make_gif(name='test')

simulation()

