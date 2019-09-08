import matplotlib.animation as animation
import matplotlib.pyplot as plt
import scipy.ndimage as ndi
import numpy as np
import resource
import imutils
import os


depth = 25
width = 250
height = 250
state = np.zeros((width, height, 3))
# Initialize

for y in range(state.shape[0]):
    for x in range(state.shape[1]):
        state[x, y, :] = [0., 0.3, 0.5]

plt.imshow(state)
plt.show()

simulation = []
for step in range(depth):
