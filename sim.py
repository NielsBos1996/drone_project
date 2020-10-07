import matplotlib.pyplot as plt
import numpy as np
import subprocess
import functools
import imageio
import time
import io
import os


def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        st = time.time()
        result = func(*args, **kwargs)
        print(f'Executing time: {time.time()-st:.4f} seconds')
        return result
    return wrapper


def test():
    x = np.array([0.])
    y = np.array([0.])
    z = np.array([0.])
    c = np.array(['blue'])

    images = []

    for time in range(100):
        buf = io.BytesIO()
        fig = scatter(x, y, time/100, c, zmin=0, zmax=1, title=f'time: {time}')
        fig.savefig(buf, format='png')
        images.append(buf)
        plt.close()
    make_gif(images, name='test')


def scatter(x, y, z, c, xmin=None, xmax=None, ymin=None, ymax=None, zmin=None,
            zmax=None, title=""):
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1, projection='3d')
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


def make_gif(images: list, name: str, show=True):
    if not name.endswith('.gif'):
        name += '.gif'
    with imageio.get_writer(name, mode='I') as writer:
        for path_to_image in images:
            path_to_image.seek(0)
            img = imageio.imread(path_to_image)
            writer.append_data(img)
    if show:
        subprocess.check_output([f'{os.getcwd()}\\{name}'], shell=True)


test()



