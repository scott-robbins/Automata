import matplotlib.animation as animation
import matplotlib.pyplot as plt
import scipy.ndimage as ndi
import numpy as np

colors = {'r': [1, 0, 0],
          'g': [0, 1, 0],
          'b': [0, 0, 1],
          'c': [0, 1, 1],
          'm': [1, 0, 1],
          'y': [1, 1, 0],
          'k': [1, 1, 1]}


def color_demo():
    rgb_test = np.zeros((2, 3, 3))
    rgb_test[0, 0, :] = colors['r']
    rgb_test[0, 1, :] = colors['g']
    rgb_test[0, 2, :] = colors['b']

    rgb_test[1, 0, :] = colors['c']
    rgb_test[1, 1, :] = colors['m']
    rgb_test[1, 2, :] = colors['y']
    plt.imshow(rgb_test)
    plt.show()


