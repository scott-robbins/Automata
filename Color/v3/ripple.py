from matplotlib.animation import FFMpegWriter
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import scipy.ndimage as ndi
import numpy as np
import imutils
import time
import sys

tic = time.time()

k0 = [[1,1,1],[1,0,1],[1,1,1]]

k1 = [[1,1,1,1],
      [1,0,0,1],
      [1,0,0,1],
      [1,1,1,1]]

k2 = [[0,0,0,0],
      [0,1,1,0],
      [0,1,1,0],
      [0,0,0,0]]

c0 = [[1,1,0],
      [1,0,0],
      [0,0,0]]

c1 = [[0,1,1],
      [0,0,1],
      [0,0,0]]

c2 = [[0,0,0],
      [0,0,1],
      [0,1,1]]

c3 = [[0,0,0],
      [1,0,0],
      [1,1,0]]

wiggles = [c0, c1, c2, c3]


def fluid_simulation(world, length, opts):
    f = plt.figure()
    simulation = []
    simulation.append([plt.imshow(world, 'gray')])
    '''<<<_( (:RUN FLUID SIMULATION:) )_>>> '''
    for dt in range(length):
        v0 = ndi.convolve(world, k0, origin=0).flatten()
        # v1 = ndi.convolve(world, k1, origin=0).flatten()
        # v2 = ndi.convolve(world, k2, origin=-0).flatten()
        ii = 0
        for cell in v0:
            [x, y] = imutils.ind2sub(ii, world.shape)
            if cell % 3 == 0:
                world[x, y] -= 1
            if v0[ii] % 4 == 0 and world[x,y] >0:
                world[x, y] += 1
            # if world[x,y] == -1 and cell % 2 ==0:
            #     world[x,y] = 1
            ii += 1
        simulation.append([plt.imshow(world, 'gray')])
    print 'Simulation Finished [%ss Elapsed]\n\033[3mRendering...\033[0m' % str(time.time()-tic)
    if opts['show']:
        a = animation.ArtistAnimation(f, simulation, blit=opts['frame_rate'], repeat_delay=900)
        if opts['save']:
            writer = FFMpegWriter(fps=10, metadata=dict(artist='Me'), bitrate=1800)
            a.save('squarely.mp4', writer=writer)
        plt.show()
    return simulation


frames = 75
width  = 100
height = 100

state = np.zeros((width, height, 3))
state[:, :, 2] = imutils.draw_centered_box(state[:, :, 2], 10, 1, False)

if len(sys.argv) > 1:
    state = plt.imread(sys.argv[1])
if len(state.shape) > 2:
    state = state[:,:,2]
print 'STARTING SIMULATION'
simulation = fluid_simulation(state, frames, {'show': True,
                                              'save': True,
                                              'frame_rate': 100})
