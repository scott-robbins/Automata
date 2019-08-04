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

DEPTH = 150


def draw_progress_bar(im, dims, depth, index):
    os.system('clear')
    print '#'*30
    print 'Loaded Images %s' % im
    print 'Dimensions of Image: %s' % str(dims)
    print 'Color Image: %s' % str(isColor)
    bar = '#'
    for b in range(int(index*31/depth)):
        bar += '#'
    if index != depth:
        print '\033[1m' + bar + ' [\033[32m'+str(100*index/depth + 1)+'% Complete\033[0m\033[1m]\033[0m'
    else:
        print '\033[1m' + bar + ' [\033[32m100% Complete\033[0m\033[1m]\033[0m'


os.system('clear')
print '#'*30
name = ''
if len(sys.argv) == 2:
    img_in = np.array(plt.imread(sys.argv[1]))
    dims = img_in.shape
    isColor = len(img_in.shape) > 2
    print 'Loaded Images %s' % sys.argv[1]
    print 'Dimensions of Image: %s' % str(dims)
    print 'Color Image: %s' % str(isColor)
    name = sys.argv[1]
    if isColor:
        img_in = img_in[:,:,0]
else:
    img_in = imutils.draw_centered_circle(np.zeros((200, 200)), 50, False)
    dims = img_in.shape
    isColor = len(img_in.shape) > 2
    print 'Loaded Circle'
    print 'Dimensions of Image: %s' % str(dims)
    print 'Color Image: %s' % str(isColor)
    name = 'Circle'
''' GENERATE '''
f = plt.figure()
state = img_in
simulation = []
for step in range(DEPTH):
    n0 = ndi.convolve(state, k0, origin=0).flatten()
    n1 = ndi.convolve(state, k1, origin=0).flatten()
    n2 = ndi.convolve(state, k2, origin=0).flatten()
    ii = 0
    state = state.flatten()
    for cell in state:
        c0 = n0[ii]
        c1 = n1[ii]
        c2 = n2[ii]
        if (c0 or c1 or c2)==8 and state[ii] == 1:
            state[ii] = 0
        if (c1 or c2) % 5 == 0:
            state[ii] -= 1
        ii += 1
    state = state.reshape((dims[0], dims[1]))
    simulation.append([plt.imshow(state, 'gray')])
    draw_progress_bar(name, dims, DEPTH, step)

simulation.reverse()    # Reversing the order looks pretty cool too!
a = animation.ArtistAnimation(f, simulation, interval=50, blit=True, repeat_delay=1000)
print '\033[1m\033[31mFINISHED\033[0m\033[1m[%ss Elapsed]\033[0m' % str(time.time()-tic)
w = FFMpegWriter(fps=5,metadata=dict(artist='Me'), bitrate=1800)
if raw_input('Do you Want to Save? (y/n): ').upper()=='Y':
    a.save(raw_input('Enter Filename: '), writer=w)
plt.show()

