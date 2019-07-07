import matplotlib.pyplot as plt
import scipy.ndimage as ndi
import numpy as np
import imutils
import time
import sys


def spawn_random_kernel(shape):
    return np.array(np.random.random_integers(0,1,shape[0]*shape[1])).reshape((shape[0],shape[1]))


def run1(ngen, seed, probability, pfactor):
    simulation = [seed]
    prob_kerns = []
    k0 = [[1,1,1],[1,0,1],[1,1,1]]
    k1 = [[]]
    dims = seed.shape
    gen = 0
    [prob_kerns.append(spawn_random_kernel([13, 13])) for k in range(probability)]
    chance = np.random.random_integers(0, 100, len(prob_kerns)) > pfactor
    flipped = np.zeros((seed.shape)).flatten()
    while gen <= ngen:
        ii = 0
        if chance[gen]:
            k = prob_kerns.pop()
        else:
            k = k0
        cells = ndi.convolve(seed, k, origin=0).flatten()
        seed = seed.flatten()
        for cell in cells:
            if seed[ii] == 255 and cell % 4 == 0 or seed[ii] == 12:
                seed[ii] = 1
                flipped[ii] += 1
            if seed[ii] == 255 and (cell % 3 == 0 or cell % 5 == 0):
                seed[ii] = 0
                flipped[ii] += 1
            elif cell % 7 == 0 or cell % 9 == 0 or seed[ii] % 4 == 0:
                seed[ii] += 1
                flipped[ii] += 1
            if flipped[ii] >= ngeneration - ngeneration/2:
                seed[ii] = 0
            if (seed[ii]==1 or seed[ii]==255) and flipped[ii] > ngeneration/2 or cell % 6 == 0:
                seed[ii] == 255
            ii += 1
        gen += 1
        seed = seed.reshape(dims)
        simulation.append(seed)
    return simulation


def blurs(ngen, seed, probability, pfactor):
    simulation = [seed]
    prob_kerns = []
    k0 = [[1,1,1],[1,0,1],[1,1,1]]
    k1 = [[]]
    dims = seed.shape
    gen = 0
    [prob_kerns.append(spawn_random_kernel([4, 4])) for k in range(probability)]
    chance = np.random.random_integers(0, 100, len(prob_kerns)) > pfactor

    while gen <= ngen:
        ii = 0
        if chance[gen]:
            k = prob_kerns.pop()
        else:
            k = k0
        cells = ndi.convolve(seed, k, origin=0).flatten()
        seed = seed.flatten()
        for cell in cells:
            if seed[ii] == 255 and cell % 2 == 0:
                seed[ii] = 1
            if seed[ii] == 255 and cell % 3 == 0:
                seed[ii] = 0
            elif cell % 8 == 0:
                seed[ii] += 1
            ii += 1
        gen += 1
        seed = seed.reshape(dims)
        simulation.append(seed)
    return simulation


t0 = time.time()
W = 250
H = 250
ngeneration = 250
cx = W/2
cy = H/2

state = np.zeros((W, H))
state = imutils.draw_centered_circle(state, W/3, False)
state[W/2-50:W/2+50, H/2-50:H/2+50] = 9
noise = np.array(np.random.random_integers(0, 1, W*H)).reshape((W, H))
slate = state+noise/2

if '-im' in sys.argv:
    slate = plt.imread(sys.argv[2])[:,:,0]

    print '%s Loaded [%d x %d]' % (sys.argv[2], slate.shape[0],slate.shape[1])
sim = run1(ngeneration,slate, 65, .65)
# sim = blurs(ngeneration, slate, ngeneration+1, 65)
print '[%s seconds Elapsed]' % str(time.time()-t0)

imutils.bw_render(sim, 50, False, 'probabilistic4.mp4')
