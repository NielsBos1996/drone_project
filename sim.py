import matplotlib.pyplot as plt
import numpy as np
import subprocess
import functools
import tempfile
import imageio
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


@execution_log
def make_plot():
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
    return images


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

@execution_log
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


img = make_plot()
make_gif(img, name='test')



