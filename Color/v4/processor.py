from matplotlib.animation import FFMpegWriter
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import scipy.ndimage as ndi
import scipy.misc as misc
import numpy as np
import imutils
import time
import sys
import os


ani_cmd = 'ffmpeg -loglevel quiet -r 20 -i pic%d.png -vcodec libx264' \
          ' -pix_fmt yuv420p cas_fractal.mp4'
clean = 'ls *.png | while read n; do rm $n; done'

tic = time.time()

k0 = [[1,1,1],[1,0,1],[1,1,1]]
k1 = [[1,1,1,1],[1,0,0,1],[1,0,0,1],[1,1,1,1]]
k2 = [[0,0,0,0],[0,1,1,0],[0,1,1,0],[0,0,0,0]]
k3 = [[1,1,1,1,1],
      [1,0,0,0,1],
      [1,0,1,0,1],
      [1,0,0,0,1],
      [1,1,1,1,1]]
k4 = [[1,1,0,1,1],
      [1,1,0,1,1],
      [0,0,1,0,0],
      [1,1,0,1,1],
      [1,1,0,1,1]]
k5 = [[0,0,1,1,0,0],
      [0,1,1,1,1,0],
      [1,1,1,1,1,1],
      [1,1,1,1,1,1],
      [0,1,1,1,1,0],
      [0,0,1,1,0,0]]
k6 = [[1,1,0,0,1,1],
      [1,0,0,0,0,1],
      [0,0,0,0,0,0],
      [0,0,0,0,0,0],
      [1,0,0,0,0,1],
      [1,1,0,0,1,1]]


def load_image():
    if len(sys.argv) >= 2:
        img_in = np.array(plt.imread(sys.argv[1]))
    else:
        img_in = np.array(plt.imread('earth.jpeg'))
    return img_in


def automata_command_line_splash(n, N):
    colors = {0: '\033[31m',
              1: '\033[32m',
              2: '\033[33m',
              3: '\033[34m',
              4: '\033[36m'}
    color = colors[np.random.random_integers(0,colors.keys().pop(-1),1)[0]]
    print '\033[1m'+color+'%ss Percent Complete' % str(100.*n/N)
    print '   ___    _    _  _______  _____    _    _      ___   _______   ___'
    print '  / _ \\  | |  | ||__   __||  _  |  / \\  / \\    / _ \\ |__   __| / _ \\'
    print ' / /_\\ \\ | |  | |   | |   | | | | / _ \\/ _ \\  / /_\\ \\   |  |  / /_\ \\'
    print '/ /   \\ \\ \\ \\_/ /   | |   | |_| |/ / \\__/ \\ \\/ /   \\ \\  |  | / /   \\ \\'
    print '\033[0m='+'='*int(10.*n/N)*8


def process_one(img_in, depth, save):
    f = plt.figure()
    frames = []
    frames.append([plt.imshow(img_in)])
    ind2sub = imutils.LIH_flat_map_creator(img_in[:, :, 0])
    print '[*] Starting Simulation [%ss Elapsed]' % str(time.time()-tic)
    for frame in range(depth):
        rch = img_in[:, :, 0]
        gch = img_in[:, :, 1]
        bch = img_in[:, :, 2]

        rc1 = ndi.convolve(rch, k0, origin=0).flatten()
        gc1 = ndi.convolve(gch, k0, origin=0).flatten()
        bc1 = ndi.convolve(bch, k0, origin=0).flatten()

        for ii in range(img_in.shape[0]*img_in.shape[1]):
            [x,y] = ind2sub[ii]
            if rc1[ii] % 4 and rch[x,y]:
                img_in[x, y, 0] = 0
                img_in[x, y, 1] = 0
                img_in[x, y, 2] = 0
            elif rc1[ii] % 7==0 and rch[x,y]:
                img_in[x, y, 0] = 0
                img_in[x, y, 1] = 0
                img_in[x, y, 2] = 1
            if bc1[ii] % 7 or bc1[ii]%6 and rch[x,y]:
                img_in[x, y, 1] = 1
                img_in[x, y, 0] = 0
            if bch[x,y] and gch[x,y]:
                if gc1[ii] % 3 == 0:
                    img_in[x, y, 0] = 1
                    img_in[x, y, 2] = 0
            if not bch[x,y] and not gch[x,y] and not bch[x,y]:
                if rc1[ii]%8==0:
                    img_in[x,y,0] = 1

        frames.append([plt.imshow(img_in)])

        if save:
            misc.imsave('pic%d.png' % frame,img_in)
        os.system('clear')
        automata_command_line_splash(frame, depth)
    print '[*] Simulation Finished [%ss Elapsed]' % str(time.time()-tic)
    a = animation.ArtistAnimation(f,frames,interval=100,blit=True,repeat_delay=900)
    print '[*] Render Finished [%ss Elapsed]' % str(time.time()-tic)
    plt.show()


automata_command_line_splash(1, 1)
width = 250
height = 250
state = np.zeros((width, height, 3))
state[:,:,0] = imutils.draw_centered_circle(state[:,:,0],width/3,1,False)
save = True
if '-in' in sys.argv:
    sys.argv.remove('-in')
    state = load_image()

process_one(state, 100, save)

if save:
    os.system(ani_cmd)
    os.system(clean)
print '[*] FINISHED [%ss Elapsed]' % str(time.time()-tic)
