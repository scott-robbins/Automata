from matplotlib.animation import FFMpegWriter
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import scipy.ndimage as ndi
import numpy as np
import imutils
import time
import os

tic = time.time()

k0 = [[1,1,1], [1,0,1], [1,1,1]]

k1 = [[1,1,1,1],
      [1,0,0,1],
      [1,0,0,1],
      [1,1,1,1]]


class Sapling:
    location = []
    internal_state = 0
    energy_level = 0

    def __init__(self, position, value, size):
        self.location = position


def sapling(state, depth, opts):
    f = plt.figure()
    reel = []
    reel.append([plt.imshow(state)])
    ind2sub = imutils.LIH_flat_map_creator(state)
    for step in range(depth):

        reel.append([plt.imshow(state)])
    print 'Simulation Finished [%ss Elapsed]' % str(time.time()-tic)
    a = animation.ArtistAnimation(f, reel, interval=opts['frame_rate'], blit=True, repeat_delay=900)
    if opts['save']:
        writer = FFMpegWriter(fps=opts['frame_rate'], metadata=dict(artist='Me'), bitrate=1800)
        a.save(opts['name'], writer=writer)
    print 'Rendering Finished [%ss Elapsed]' % str(time.time()-tic)
    plt.show()


w = 250
h = 250
depth = 100

# Create a Noise Floor for the saplinig to draw energy from
cx = int(w/2)
cy = int(h/2)
state = np.random.random_integers(0, 25, w*h).reshape((w, h))
# state += imutils.draw_centered_box(state, 15, 255, False)
seed = Sapling(position=[cx, cy], value=255, size=3)

# Run it
sapling(state, depth, {'frame_rate': 50, 'save': True, 'name': 'crystalize1.mp4'})
