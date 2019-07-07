from matplotlib.animation import FFMpegWriter
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import scipy.ndimage as ndi
import numpy as np
import imutils
import time
import sys

tic = time.time()
k0 = [[1,1,1],[1,1,1],[1,1,1]]


def create_color_pt_cloud(state, color, n_points):

    for i in range(n_points):
        [x, y] = imutils.spawn_random_point(np.zeros((width, height)))
        if color == 'R':
            state[x,y,0] = 1
        if color == 'G':
            state[x,y,1] = 1
        if color == 'B':
            state[x,y,2] = 1
    return state


def LIH_flat_map_creator(state):
    """
    LoopInvariantHoisting to preallocate a map, that
    pairs a flattened index of a corresponding state to
    an x-y position.
    :param state:
    :return:
    """
    index_map = {}
    for index in range(state.shape[0]*state.shape[1]):
        index_map[index] = imutils.ind2sub(index, [state.shape[0], state.shape[1]])
    return index_map


def probabilistic_cloud(state, weights, n_generations, frame_rate, file_name):
    print '\t\t\033[1m\033[3m** STARTING SIMULATION **\033[0m'
    f = plt.figure()
    gen = 0
    simulation = list()
    simulation.append([plt.imshow(state)])

    ind2sub = LIH_flat_map_creator(state)

    while gen < n_generations:
        rworld = ndi.convolve(state[:,:,0], k0, origin=0)
        gworld = ndi.convolve(state[:,:,1], k0, origin=0)
        bworld = ndi.convolve(state[:,:,2], k0, origin=0)

        for ind in range(len(rworld.flatten())):
            [x, y] = ind2sub[ind]
            if bworld[x, y] % 4 == 0:
                state[x, y] = [1, 0, 0]
            if rworld[x, y] % 4 == 0 and (bworld[x, y] and rworld[x,y]) >= 4:
                state[x, y] = [1, 0, 1]
            # If magenta, and R(ii)/B(ii) % 5 make yellow
            if (state[x, y][0] and state[x, y][2]) == 1 and state[x, y][1] == 0 and (rworld[x,y] or bworld[x,y]) % 5 == 0:
                state[x, y] = [1, 1, 0]
            # If cyan, and R(ii)/B(ii) % 5 make green
            if (state[x, y][1] and state[x, y][2]) == 1 and state[x, y][0] == 0 and (gworld[x,y] or bworld[x,y]) % 4 == 0:
                state[x,y] = [0,1,0]

        gen += 1
        simulation.append([plt.imshow(state)])
    '''   ANIMATE '''
    a = animation.ArtistAnimation(f,simulation,interval=350,blit=True,repeat_delay=900)
    print 'FINISHED [%ss Elapsed]' % str(time.time() - tic)
    writer = FFMpegWriter(fps=frame_rate, metadata=dict(artist='Me'), bitrate=1800)
    a.save(file_name, writer=writer)
    plt.show()


''' STATE INITIALIZATION '''
width = 150
height = 150
state = np.zeros((width, height, 3))
n_points_total = 1000
box = imutils.draw_centered_box(np.zeros((width, height)), 65, 1, False)
circ = imutils.draw_centered_circle(np.zeros((width, height)), 45, 1, False)
'''  RUN SIMULATION '''
initial_state = create_color_pt_cloud(state, 'B', n_points_total)
initial_state[:,:,2] = box
initial_state[:,:,1] = circ
probabilistic_cloud(initial_state, [0.9, 0.8,0.5], 120, 350, 'ColorAutomata4.mp4')

