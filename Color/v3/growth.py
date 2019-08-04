from matplotlib.animation import FFMpegWriter
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import scipy.ndimage as ndi
import numpy as np
import imutils
import time
import sys

tic = time.time()


def grow(state,pos,rch,gch,bch):
    x = pos[0]
    y = pos[1]

    if state[x,y,0] == 0 and state[x,y,1]==1 and state[x,y,2] == 0 and bch[x,y] > gch[x,y]:
        state[x,y,:] = [1,0,1]
    if state[x, y, 0] ==0 and state[x, y, 1] ==0 and state[x, y, 2] ==0 and gch[x,y] % 5 ==0 and rch[x,y] < 4:
        state[x,y,:] = [1,0,0]
    return state


def simulation(state, depth, saveData):
    f = plt.figure()
    simulation = list()
    simulation.append([plt.imshow(state)])
    k0 = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]

    ind2sub = imutils.LIH_flat_map_creator(state)
    gen = 0
    while gen <= depth:
        rworld = ndi.convolve(state[:, :, 0], k0, origin=0)
        gworld = ndi.convolve(state[:, :, 1], k0, origin=0)
        bworld = ndi.convolve(state[:, :, 2], k0, origin=0)

        for px in range(state.shape[0]*state.shape[1]):
            state = grow(state, ind2sub[px], rworld, gworld, bworld)
        simulation.append([plt.imshow(state)])
        gen += 1

    print 'FINISHED [%ss Elapsed]' % str(time.time() - tic)
    a = animation.ArtistAnimation(f,simulation,interval=saveData['frame_rate'],blit=True,repeat_delay=500)
    if saveData['save']:
        writer = FFMpegWriter(fps=saveData['fps'], metadata=dict(artist='Me'), bitrate=1800)
        a.save(saveData['file_name'], writer=writer)
    plt.show()
    return state


''' DEFINE SIMULATION STATE '''
width = 100
height = 100
state = np.zeros((width, height, 3))
state[:,:,2] = imutils.draw_centered_box(np.zeros((width, height)),20,1,False)
state[:,:,1] = imutils.draw_centered_box(np.zeros((width, height)),30,1,False)
state[:,:,:] -= imutils.draw_centered_circle(np.zeros((width, height, 3)),10,1,False)

config = {'frame_rate': 150,
          'fps': 10,
          'save': False,
          'file_name': '.mp4',
          'origin': [50, 50]}
simulation(state, depth=100, saveData=config)
