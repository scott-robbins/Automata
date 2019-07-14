from matplotlib.animation import FFMpegWriter
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import scipy.ndimage as ndi
import numpy as np
import imutils
import time
import sys

tic = time.time()


def simulation(state, depth, saveData):
    f = plt.figure()
    simulation = list()
    simulation.append([plt.imshow(state)])
    k0 = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]
    ind2sub = imutils.LIH_flat_map_creator(state)
    '''
    With this model, the actual automata rules can be functionalized, which
    should help me generate tests more rapidly and also hold onto the more 
    interesting rule sets (which often get lost during modification)
    '''

    gen = 0
    while gen <= depth:
        rworld = ndi.convolve(state[:, :, 0], k0, origin=0)
        gworld = ndi.convolve(state[:, :, 1], k0, origin=0)
        bworld = ndi.convolve(state[:, :, 2], k0, origin=0)

        for px in range(state.shape[0]*state.shape[1]):
            simulation.append([plt.imshow(state)])
        gen += 1

    print 'FINISHED [%ss Elapsed]' % str(time.time() - tic)
    a = animation.ArtistAnimation(f,simulation,interval=saveData['frame_rate'],blit=True,repeat_delay=500)
    if saveData['save']:
        writer = FFMpegWriter(fps=saveData['frame_rate'], metadata=dict(artist='Me'), bitrate=1800)
        a.save(saveData['file_name'], writer=writer)
    plt.show()
    return state


''' DEFINE SIMULATION STATE '''
width = 100
height = 100
state = np.zeros((width, height, 3))

