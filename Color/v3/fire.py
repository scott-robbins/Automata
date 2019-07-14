from matplotlib.animation import FFMpegWriter
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import scipy.ndimage as ndi
import numpy as np
import imutils
import time
import sys

tic = time.time()


def fire_starter(state, flipped, rch, gch, bch, k, pos):
    x = pos[0]
    y = pos[1]

    if state[x,y,0] == 0 and state[x,y,1] == 0 and state[x,y,2] == 0 and rch[x, y] >= 9:
        state[x, y, :] = [1,0,0]
        flipped[x,y] += 1
    if state[x, y, 0] == 0 and state[x, y, 1] == 0 and state[x, y, 2] == 0 and (gch[x, y] % 8 or bch[x, y] % 6) == 0:
        state[x, y, :] = [1, 0, 0]
    elif rch[x,y] % 8 == 0 or flipped[x,y]>=10 and state[x, y, 0] == 0 and state[x, y, 1] == 0 and state[x, y, 2] == 0:
        state[x,y,:] = [1,1,0]
        flipped[x, y] += 1
    elif (gch[x, y] % 7) == 0:
        state[x, y, :] = [1, 0, 1]
        flipped[x, y] += 1
    if rch[x,y] >= 4 and bch[x,y] >= 4:
        state[x,y,:] = [0,0,0]
    return state


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
    flipped = np.zeros((state.shape[0], state.shape[1]))
    gen = 0
    while gen <= depth:
        rworld = ndi.convolve(state[:, :, 0], k0, origin=0)
        gworld = ndi.convolve(state[:, :, 1], k0, origin=0)
        bworld = ndi.convolve(state[:, :, 2], k0, origin=0)

        for px in range(state.shape[0]*state.shape[1]):
            state = fire_starter(state, flipped, rworld, gworld, bworld, k0, ind2sub[px])
        simulation.append([plt.imshow(state)])
        # state[:, :, 0] += imutils.draw_centered_circle(state[:, :, np.random.random_integers(0,2,1)[0]], 5 , 1, False)
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
state[:,:,0] += imutils.draw_centered_circle(state[:,:,0],10,1,False)
state[:,:,2] += imutils.draw_centered_box(state[:,:,0],20,2,False)
config = {'frame_rate': 150,
          'fps': 10,
          'save': True,
          'file_name': 'flashy_0.mp4',
          'origin': [50, 50]}
simulation(state, depth=100, saveData=config)
