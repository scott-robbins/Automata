from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
import matplotlib.pyplot as plt
import scipy.ndimage as ndi
import numpy as np
import imutils
import time
import os

tic = time.time()
shades = {1: 'red',
          2: 'green',
          3: 'blue',
          4: 'cyan',
          5: 'magenta',
          6: 'orange',
          7: 'yellow',
          8: 'purple'}

ani_cmd = 'ffmpeg --loglevel quiet -r 6 -i pic%d.png -vcodec libx264 -pix_fmt' \
          ' yuv420p automata3d_2.mp4'

k0 = [[1,1,1],[1,0,1],[1,1,1]]
k1 = [[1,1,1,1],[1,0,0,1],[1,1,1,1]]
# Simulation Parameters
width = 25
height = 25
length = 15
flat_state = np.zeros((width, height))
initial_state = np.array(imutils.draw_centered_box(flat_state, int(width/8), 1, False)) > 0

# Create 3D Space
x, y, z = np.indices((width, height, 25))

f = plt.figure()
ax = f.gca(projection='3d')
for step in range(length):
    box = imutils.draw_centered_box(flat_state, int(width / (step+2)), 1, False)
    box -= np.random.random_integers(0,1,width*height).reshape((width, height)) > 0
    initial_state = np.array(box) > 0
    shape = (z < step +3) & initial_state[x, y] & (z >= step)
    if step > 0:
        voxel = voxel | shape
    else:
        voxel = shape

    colors = np.empty(voxel.shape, dtype=object)
    colors[shape] = 'green'
    ax.voxels(voxel, facecolors=colors, edgecolors='k')
    plt.savefig('pic%d.png' % step)
    plt.cla

print '\033[1mSimulation Finished[%ss Elapsed]\n033[3mRendering... \033[0m' % str(time.time()-tic)
os.system(ani_cmd)
os.system('clear; ls *.png | while read n; do rm $n; done')
os.system('vlc automata3d_2.mp4')
