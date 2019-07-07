from matplotlib.animation import FFMpegWriter
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import scipy.ndimage as ndi
import numpy as np
import imutils
import time
import sys
import os

tic = time.time()

R = [1,0,0]
G = [0,1,0]
B = [0,0,1]
K = [0,0,0]
W = [1,1,1]
C = [0,1,1]
M = [1,0,1]
Y = [1,1,0]

CMAP = {1: R, 2: G, 3: B,
        4: C, 5: M, 6: Y,
        7: K, 8: W}

TRANSITIONS = {1: [5, 6],
               2: [4, 6],
               3: [4, 5],
               8: [1, 2, 3, 4, 5, 6]}

k0 = [[1,1,1],[1,1,1],[1,1,1]]
k1 = [[1,1,1],[1,0,1],[1,1,1]]
k2 = [[1,1,1,1],[1,0,0,1],[1,0,0,1],[1,1,1,1]]
k3 = [[0,0,0,0],[0,1,1,0],[0,1,1,0],[0,0,0,0]]


gen = 0
n_gen = 100
width = 50
height = 50
state = np.zeros((width, height, 3))
simulation = []
f = plt.figure()

r_noise = np.random.random_integers(0, 2, width * height).reshape((width, height))
g_noise = np.random.random_integers(0, 2, width * height).reshape((width, height))
b_noise = np.random.random_integers(0, 2, width * height).reshape((width, height))
print '\033[1m\033[3m** STARTING SIMULATION **\033[0m'
if '-r' in sys.argv:

    state[:, :, 0] = r_noise
    state[:, :, 1] = g_noise
    state[:, :, 2] = b_noise

if '-retro' in sys.argv:
    r_noise = imutils.draw_centered_circle(state[:, :, 0], 22, 1, False)
    g_noise = imutils.draw_centered_circle(state[:, :, 1], 14, 1, False)
    b_noise = imutils.draw_centered_box(state[:, :, 2], 8, 1, False)

    state[:, :, 0] = r_noise
    state[:, :, 1] = g_noise
    state[:, :, 2] = b_noise

simulation.append([plt.imshow(state)])
try:
    for gen in range(n_gen):

        dims = state.shape

        r_world = ndi.convolve(r_noise, np.ones((3,3)), origin=0).flatten()
        g_world = ndi.convolve(g_noise, np.ones((3,3)), origin=0).flatten()
        b_world = ndi.convolve(b_noise, np.ones((3,3)), origin=0).flatten()

        r_noise = r_noise.flatten()
        g_noise = g_noise.flatten()
        b_noise = b_noise.flatten()

        for px in range(width * height):
            rpxl = r_noise[px]
            gpxl = g_noise[px]
            bpxl = b_noise[px]

            pixel = [rpxl, gpxl, bpxl]

            if pixel == R and r_world[px] % 8 == 0:
                pixel = [1,0,1]
            if pixel == G and g_world[px] % 8 == 0:
                pixel = [1,1,0]
            if pixel == B and b_world[px] % 8 == 0:
                pixel = [0,1,1]
            if pixel == C and r_world[px] >= 5:
                if np.random.random_integers(0,10,1)[0]>5:
                    pixel = [0,0,1]
                else:
                    pixel = [0,1,0]
            if pixel == M and g_world[px] >= 5:
                if np.random.random_integers(0,10,1)[0]>5:
                    pixel = [1,0,0]
                else:
                    pixel = [0,0,1]
            if pixel == Y and b_world[px] >= 5:
                if np.random.random_integers(0,11,1)[0]>5:
                    pixel = [1,0,0]
                else:
                    pixel = [0,1,0]
            if pixel == K and (r_world[px]or g_world[px]or b_world[px]) >= 5:
                flip = np.random.random_integers(0,11,1)[0]
                if flip <= 3:
                    pixel = [1,0,0]
                if 6 >+ flip > 3:
                    pixel = [0,1,0]
                if flip > 6:
                    pixel = [0,0,1]
            if pixel == W:
                flip = np.random.random_integers(0, 11, 1)[0]
                if flip <= 3:
                    pixel = [1, 0, 0]
                if 6 > + flip > 3:
                    pixel = [0, 1, 0]
                if flip > 6:
                    pixel = [0, 0, 1]
                if r_world[px] == 8:
                    pixel = [1,0,0]
                if g_world[px] == 8:
                    pixel = [0,1,0]
                if b_world[px] == 8:
                    pixel = [0,0,1]
                if (r_world[px] and g_world[px] and b_world[px] % 6) == 0:
                    pixel = [0,0,0]
            # TODO: handle K,W

            [x, y] = imutils.ind2sub(px, [width, height])
            state[x, y, :] = pixel
            px += 1
        r_noise = r_noise.reshape((dims[0],dims[1]))
        g_noise = g_noise.reshape((dims[0],dims[1]))
        b_noise = b_noise.reshape((dims[0],dims[1]))
        simulation.append([plt.imshow(state)])
        gen += 1
except KeyboardInterrupt:
    print gen
    pass

print '\033[1mSIMULATION FINISHED [%ss Elapsed]\033[0m' % str(time.time()-tic)
a = animation.ArtistAnimation(f,simulation,interval=85,blit=True,repeat_delay=900)
# writer = FFMpegWriter(fps=100, metadata=dict(artist='Me'), bitrate=1800)
# a.save('ColorAutomata.mp4', writer=writer)
plt.show()