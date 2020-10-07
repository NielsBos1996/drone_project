import matplotlib.pyplot as plt
import numpy as np
import io
import imageio
from PIL import Image


def scatter(x, y, z, c):
    n = 100
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.scatter(x, y, z, c=c)
    return fig


def test():
    x = np.array([0.])
    y = np.array([0.])
    z = np.array([0.])
    c = np.array(['blue'])

    images = []

    for time in range(100):
        z[0] = time / 100

        fig = plt.figure()
        ax = fig.add_subplot(1,1,1, projection='3d')
        ax.scatter(x, y, z, c)
        ax.set_zlim(0, 1)

        # fig = scatter(x, y, z, c)
        # fig.set_zlim(0, 1)
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        images.append(buf)
        plt.close()

    with imageio.get_writer('./test_drone.gif', mode='I') as writer:
        for path_to_image in images:
            path_to_image.seek(0)
            img = imageio.imread(path_to_image)
            writer.append_data(img)

test()



