from matplotlib.animation import FFMpegWriter
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import scipy.ndimage as ndi
import numpy as np
import imutils
import time
import sys


width  = 100
height = 100
state = np.zeros((width, height, 3))
state[:,:,2] = 1


