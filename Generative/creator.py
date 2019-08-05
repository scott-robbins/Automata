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

k0 = [[1,1,1],[1,0,1],[1,1,1]]
k1 = [[1,1,1,1],[1,0,0,1],[1,0,0,1],[1,1,1,1]]
k2 = [[0,0,0,0,0],
      [0,1,1,1,0],
      [0,1,1,1,0],
      [0,1,1,1,0],
      [0,0,0,0,0]]

DEPTH = 75


def draw_progress_bar(im, dims, depth, index):
    os.system('clear')
    print '\033[1m'+'#'*8+' << \033[31m\033[3mCREATOR\033[0m\033[1m >> '+'#'*8+'\033[0m'
    print '[*] Loaded Image %s' % im
    print '[*] Dimensions: %s' % str(dims)
    print '[*] Color: %s' % str(isColor)
    print '[*] N Steps: %d' % DEPTH

    bar = '#'
    for b in range(int(index*31/depth)):
        bar += '#'
    if index != depth:
        print '\033[1m' + bar + ' [\033[32m'+str(100*index/depth + 1)+'% Complete\033[0m\033[1m]\033[0m'
    else:
        print '\033[1m' + bar + ' [\033[32m100% Complete\033[0m\033[1m]\033[0m'


def simulation_one(state, size, title, save):
    f = plt.figure()
    simulation = []
    simulation.append([plt.imshow(state, 'gray')])
    for step in range(DEPTH):
        n0 = ndi.convolve(state, k0, origin=0).flatten()
        n1 = ndi.convolve(state, k1, origin=0).flatten()
        n2 = ndi.convolve(state, k2, origin=0).flatten()
        ii = 0
        state = state.flatten()
        threshold = 128
        for cell in state:
            c0 = n0[ii]
            c1 = n1[ii]
            c2 = n2[ii]
            if (c0 or c1 or c2) % 8 == 0 and cell < threshold:
                state[ii] -= 10
            if (c1 or c2) % 5 == 0:
                state[ii] += 1
            if 0 < (c2 or c1 or c0) < 7 and cell >= threshold:
                state[ii] -= 1
            ii += 1
        state = state.reshape((dims[0], dims[1]))
        simulation.append([plt.imshow(state, 'gray')])
        draw_progress_bar(title, size, DEPTH, step)

    simulation.reverse()  # Reversing the order looks pretty cool too!
    a = animation.ArtistAnimation(f, simulation, interval=50, blit=True, repeat_delay=1000)
    print '\033[1m\033[31mFINISHED\033[0m\033[1m\t[%ss Elapsed]\033[0m' % str(time.time() - tic)
    if save:
        w = FFMpegWriter(fps=10, metadata=dict(artist='Me'), bitrate=1800)
        a.save('simulation_0.mp4', writer=w)
    plt.show()


def simulation_two(state, size, title):
    f = plt.figure()
    simulation = []
    for step in range(DEPTH):
        n0 = ndi.convolve(state, k0, origin=0).flatten()
        n1 = ndi.convolve(state, k1, origin=0).flatten()
        n2 = ndi.convolve(state, k2, origin=0).flatten()
        ii = 0
        state = state.flatten()
        for cell in state:
            ii += 1
        state = state.reshape((dims[0], dims[1]))
        simulation.append([plt.imshow(state, 'gray')])
        draw_progress_bar(title, size, DEPTH, step)

    simulation.reverse()  # Reversing the order looks pretty cool too!
    a = animation.ArtistAnimation(f, simulation, interval=50, blit=True, repeat_delay=1000)
    print '\033[1m\033[31mFINISHED\033[0m\033[1m\t[%ss Elapsed]\033[0m' % str(time.time() - tic)
    w = FFMpegWriter(fps=15, metadata=dict(artist='Me'), bitrate=1800)
    a.save('simulation_1.mp4', writer=w)
    plt.show()


if __name__ == '__main__':
    os.system('clear')
    print '\033[1m' + '#' * 31 + '\033[0m'
    name = ''
    if len(sys.argv) == 2:
        img_in = np.array(plt.imread(sys.argv[1]))
        dims = img_in.shape
        isColor = len(img_in.shape) > 2
        print '[*] Loaded %s' % sys.argv[1]
        print '[*] Dimensions: %s' % str(dims)
        print '[*] Color: %s' % str(isColor)
        print '[*] N Steps: %d' % DEPTH
        name = sys.argv[1]
        if isColor:
            img_in = img_in[:, :, 0]
        noise = np.random.random_integers(0, 5, img_in.shape[0] * img_in.shape[1]).reshape(
            (img_in.shape[0], img_in.shape[1]))
        img_in -= np.array(noise).astype(np.uint)
    else:
        img_in = imutils.draw_centered_circle(np.zeros((200, 200)), 50, False)
        dims = img_in.shape
        isColor = len(img_in.shape) > 2
        print '[*] Loaded Circle'
        print '[*] Dimensions: %s' % str(dims)
        print '[*] Color: %s' % str(isColor)
        print '[*] N Steps: %d' % DEPTH
        name = 'Circle'

    ''' # Running  Simulation One # '''
    simulation_one(img_in, dims, name, save=True)

# EOF
