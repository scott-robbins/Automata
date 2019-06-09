import matplotlib.pyplot as plt
import scipy.ndimage as ndi
import numpy as np
import scipy.misc
import imutils
import time
import sys
import os


def exp0(ngen,state):
    t0 = time.time()
    simulation = [state]
    gen = 0
    while gen < config['ngen']:
        cells = ndi.convolve(state, [[1, 1, 1], [1, 1, 1], [1, 1, 1]])
        avg = cells.mean()
        nextstate = state.flatten()
        flipped = state.flatten()
        ii = 0
        for cell in cells.flatten():
            if cell > avg or cell % 5 == 0 or cell % 9 == 0:
                nextstate[ii] = 1
                flipped[ii] += 1
            if cell % 3 == 0 or cell % 8 == 0 and nextstate[ii] == 255:
                nextstate[ii] = 1
                flipped[ii] += 1
            if cell % 6 == 0 or cell % 5 == 0 or cell % 7 == 0 or nextstate[ii] == 1:
                nextstate[ii] = 255
                flipped[ii] += 1
            if gen > ngen/2:
                if flipped[ii] > ngen - ngen/3:
                    nextstate[ii] = 255
            ii += 1
        gen += 1
        simulation.append(nextstate.reshape(state.shape))
        state = nextstate.reshape(state.shape)
    dt = time.time() - t0
    print '[1mSimulation Finished \033[1m[%s seconds Elapsed]\033[0m' % (time.time() - t0)
    return dt, simulation



W = 250
H = 250
if '-set_dims' in sys.argv:
    W = int(input('Enter Width: '))
    H = int(input('Enter Height: '))

state = np.random.random_integers(1,16,W*H).reshape((W, H))
state = imutils.draw_centered_circle(state,state.shape[0]/3,False)
config = {'ngen': 20,
          'n_points': 500}
if '-state' in sys.argv and len(sys.argv) == 3:
    state = np.array(scipy.misc.imread(sys.argv[2])[:,:,0])
print state.shape

dt, simulation = exp0(ngen=config['ngen'], state=state)
imutils.bw_render(simulation, 250, True, 'test2.mp4')
