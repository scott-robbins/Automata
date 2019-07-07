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


def probabilistic_cloud(state, n_generations, frame_rate, file_name):
    print '\t\t\033[1m\033[3m** STARTING SIMULATION **\033[0m'
    f = plt.figure()
    gen = 0
    simulation = list()
    simulation.append([plt.imshow(state)])

    ind2sub = imutils.LIH_flat_map_creator(state)

    while gen < n_generations:
        rworld = ndi.convolve(state[:,:,0], k0, origin=0)
        gworld = ndi.convolve(state[:,:,1], k0, origin=0)
        bworld = ndi.convolve(state[:,:,2], k0, origin=0)

        for ind in range(len(rworld.flatten())):
            [x, y] = ind2sub[ind]

            # END CATCH ALLS (Energize State/Churners)
            if bworld[x, y] % 5 == 0:
                state[x, y] = [0, 1, 1]
            if rworld[x, y] % 5 == 0 and (bworld[x, y] and rworld[x, y]) == 8:
                state[x, y] = [1, 0, 1]
            if gworld[x, y] % 5 and (bworld[x, y] and rworld[x, y]) % 4 != 0:
                state[x, y] = [1, 0, 0]

            # If magenta
            if (state[x, y][0] and state[x, y][2]) == 1 and state[x, y][1] == 0:
                # R(ii)/B(ii) % 5 make yellow
                if rworld[x,y] % 5 == 0:
                    state[x, y] = [1, 0, 0]
                elif bworld[x,y] % 5 == 0:
                    state[x, y] = [0, 0, 1]
                elif rworld[x, y] % 5 == 0:
                    state[x, y] = [0, 1, 1]
            # If cyan
            if (state[x, y][1] and state[x, y][2]) == 1 and state[x, y][0] == 0:
                # If R(ii) / B(ii) % 5 make green
                if gworld[x, y] % 5 == 0:
                    state[x, y] = [0, 1, 0]
                elif bworld[x, y] % 4 == 0:
                    state[x, y] = [1, 1, 1]
                elif rworld[x, y] % 4 == 0:
                    state[x, y] = [1, 1, 0]
            # If White? ( Here's where it can get REALLY cool I think
        gen += 1
        simulation.append([plt.imshow(state)])

    '''   ANIMATE '''
    a = animation.ArtistAnimation(f,simulation,interval=550,blit=True,repeat_delay=900)
    print 'FINISHED [%ss Elapsed]' % str(time.time() - tic)
    writer = FFMpegWriter(fps=frame_rate, metadata=dict(artist='Me'), bitrate=1800)
    a.save(file_name, writer=writer)
    plt.show()


if __name__ == '__main__':
    ''' STATE INITIALIZATION '''
    width = 150
    height = 150
    state = np.zeros((width, height, 3))
    n_points_total = 1000
    box = imutils.draw_centered_box(np.zeros((width, height)), 65, 1, False)
    circ = imutils.draw_centered_circle(np.zeros((width, height)), 45, 1, False)
    b1 = imutils.draw_centered_circle(np.zeros((width, height)), 25, 1, False)

    '''  RUN SIMULATION '''
    initial_state = create_color_pt_cloud(state, 'R', n_points_total)
    initial_state[:, :, 2] += circ
    initial_state[:, :, 1] += box
    initial_state[:, :, 0] += b1

    probabilistic_cloud(initial_state, 200, 250, 'ColorAutomata5.mp4')


