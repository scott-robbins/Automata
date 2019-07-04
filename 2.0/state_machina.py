from matplotlib.animation import FFMpegWriter
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import scipy.ndimage as ndi
import numpy as np
import imutils
import sys


def growth_simulate(state, n_steps, doSave):
    f = plt.figure()
    history = [state]
    simulation = []
    simulation.append([plt.imshow(state,'gray')])
    for i in range(n_steps):
        world = ndi.convolve(state, np.ones((3, 3)))
        for x in range(state.shape[0]):
            for y in range(state.shape[1]):
                if world[x,y] == 2:
                    state[x,y] = 1
                # if world[x, y] == 3:
                #     state[x, y] += 1
                if world[x, y]  == 4 == 0:
                    state[x, y] = 0
        simulation.append([plt.imshow(state,'gray')])
        history.append(state)
    a = animation.ArtistAnimation(f,simulation,interval=100,blit=True,repeat_delay=900)
    if doSave['do']:
        writer = FFMpegWriter(fps=doSave['fps'], metadata=dict(artist='Me'), bitrate=1800)
        a.save(doSave['name'], writer=writer)
    plt.show()
    return history


''' DEFINE DIMENISONS'''
w = 250
h = 250

state = np.zeros((w, h))
state = imutils.draw_centered_circle(state,20,2,False)
state = imutils.draw_centered_box(state,10,1,False)
plt.close()
if 'growth' in sys.argv:
    save = {'do':True,'name':'fractal_fire_0.mp4','fps':100}
    simulation = growth_simulate(state, 150, save)
