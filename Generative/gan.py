import matplotlib.pyplot as plt
import scipy.ndimage as ndi
import numpy as np
import imutils
import time
import sys

t0 = time.time()

width = 250
height = 250

if len(sys.argv) == 2:
    file_name = sys.argv[1]
    im = plt.imread(file_name)
    width = im.shape[0]
    height = im.shape[1]
    imean = np.array(im) >= 2
    rand_seed = imean[:,:,2] - np.random.random_integers(0, 1, width * height).reshape((width, height))
else:
    rand_seed = np.random.random_integers(0, 1, width * height).reshape((width, height))
activation = 4
depth = 50
k = [[1,1,1],[1,0,1],[1,1,1]]
state = np.array(rand_seed)

simulation = []
dims = state.shape
gen = 0
while gen < depth:
    world = ndi.convolve(state, k, origin=0)
    avg = world.mean()
    state = state.flatten()
    ii = 0
    for cell in world.flatten():
        try:
            if cell > activation and state[ii] == 0:
                state[ii] = 1
            if cell == activation and state[ii] == 0:
                state[ii] += 1
            if cell < activation/2 and state[ii] == 1:
                state[ii] = 0
            if cell == activation and state[ii] == 1:
                state[ii] -= 1
            if cell == 8 and state[ii] ==0 or cell == avg:
                state[ii] = 1
        except:
            pass
        ii += 1
    state = state.reshape((dims))
    simulation.append(np.abs(state))
    gen += 1
print 'FINISHED [%ss Elapsed]' % str(time.time()-t0)
imutils.bw_render(simulation, 50, True, 'automazon.mp4')
