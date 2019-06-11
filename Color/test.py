import matplotlib.pyplot as plt
import scipy.ndimage as ndi
import scipy as scipy
import numpy as np
import imutils
import time

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


def state_breakdown(state):
    f, ax = plt.subplots(1, 4)
    ax[0].imshow(state)
    ax[0].set_title('Seed')
    ax[1].imshow(state[:,:,0])
    ax[1].set_title('R Channel')
    ax[2].imshow(state[:,:,1])
    ax[2].set_title('G Channel')
    ax[3].imshow(state[:,:,2])
    ax[3].set_title('B Channel')
    plt.show()


def run(ngen, seed, filter, save):
    t0 = time.time()
    simulation = [seed]
    gen = 0
    while gen <= ngen:
        c1 = ndi.convolve(seed[:, :, 0], filter, origin=0).flatten()
        c2 = ndi.convolve(seed[:, :, 1], filter, origin=0).flatten()
        c3 = ndi.convolve(seed[:, :, 2], filter, origin=0).flatten()

        dims = seed.shape

        n1 = seed[:,:,0].flatten()
        n2 = seed[:,:,1].flatten()
        n3 = seed[:,:,2].flatten()

        i1 = 0
        i2 = 0
        i3 = 0

        for c1s in c1:
            if c1s % 3 == 0:
                n1[i1] -= 1
            if c1s % 5 == 0:
                n1[i1] += 1
            if n1[i1] == 255 and c2s % 4 == 0:
                n1[i1] -= 10
            i1 += 1
        for c2s in c2:
            if c2s % 3 == 0:
                n2[i2] = 1
            if c2s % 5 == 0 and n2[i2]==1:
                n2[i2] = 255
            i2 += 1
        for c3s in c3:
            if c3s % 3 == 0:
                n3[i3] -= 1
            if c3s % 5 == 0:
                n3[i3] += 1
            i3 += 1

        seed[:, :, 0] = n1.reshape((dims[0],dims[1]))
        seed[:, :, 1] = n2.reshape((dims[0],dims[1]))
        seed[:, :, 2] = n3.reshape((dims[0],dims[1]))
        simulation.append(seed)
        gen += 1
    print '\033[1mFinished Simulation [%s s Elapsed]\033[0m' % (time.time() - t0)
    if save:
        imutils.color_render(simulation, 150, True, 'color_automata.mp4')
    else:
        imutils.color_render(simulation, 150, False, 'color_automata.mp4')
    return simulation


def main():
    state = np.array(scipy.misc.imread('tree.jpeg'))[0:572, 160:460]
    W = state.shape[0]
    H = state.shape[1]

    print "Loaded Image [%s x %s]" % (W, H)

    # W = 250
    # H = 250  # TODO: Add opt for user defined size
    p1 = np.random.random_integers(0, 255, W * H).reshape((W, H)) >= 128
    p2 = np.random.random_integers(0, 255, W * H).reshape((W, H)) >= 128
    p3 = np.random.random_integers(0, 255, W * H).reshape((W, H)) >= 128

    # state = np.zeros((W, H, 3))
    # state[:, :, 0] = p1
    # state[:, :, 1] = p2
    # state[:, :, 2] = p3
    # state_breakdown(state)

    k0 = [[1,1,1,1],
          [1,0,0,1],
          [1,0,0,1],
          [1,1,1,1]]

    run(20, state, k0, False)


if __name__ == '__main__':
    main()

