import io
import subprocess

import matplotlib.pyplot as plt
import imageio

from src.solver import Solver
from src.helpers import *


class DroneSimulaterPlot:
    def __init__(self):
        self.images = []

    def make_plot(self, solver: Solver):
        for t in range(solver.max_time):
            fig, ax = self.init_fig(-5, 5, -5, 5, 0, 10,
                                    f"time: {len(self.images)/10} seconds")
            for d in solver.space.drone_locs[t]:
                ax.scatter(*d, c='blue')
            buf = io.BytesIO()
            fig.savefig(buf, format='png')
            self.images.append(buf)
            plt.close()
        self.make_gif("../data/images/temp")

    @staticmethod
    def scatter(x, y, z, c, xmin=None, xmax=None, ymin=None, ymax=None,
                zmin=None, zmax=None, title=""):
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

    def init_fig(self, xmin=None, xmax=None, ymin=None, ymax=None,
                 zmin=None, zmax=None, title=""):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        if xmin is not None and xmax is not None:
            ax.set_xlim(xmin, xmax)
        if ymin is not None and ymax is not None:
            ax.set_ylim(ymin, ymax)
        if zmin is not None and zmax is not None:
            ax.set_zlim(zmin, zmax)
        if title:
            ax.set_title(title)
        return fig, ax

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

if __name__ == "__main__":
    s=Solver("../data/targets/two_drones.json", drone_count=2, min_distance=1)
    s.solve()

    DSP = DroneSimulaterPlot()
    DSP.make_plot(s)
