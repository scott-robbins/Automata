from matplotlib.animation import FFMpegWriter
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import scipy.ndimage as ndi
import scipy.misc as misc
import numpy as np
import imutils
import time
import os


tic = time.time()
file_name_out = 'color_automata_simulation_0.mp4'
ani_cmd = 'ffmpeg -loglevel quiet -r 10 -i img%d.png -vcodec libx264 -pix_fmt yuv420p ' + file_name_out
clean = 'ls *.png | while read n; do rm $n; done'

pic_1 = '/home/tylersdurden/Monero/monero/external/trezor-common/defs/bitcoin/bitcoin.png'
pic_2 = 'earth.jpeg'
pic_3 = 'cat.jpeg'

k0 = [[1,1,1],[1,0,1],[1,1,1]]
k1 = [[1,1,1,1],[1,0,0,1],[1,0,0,1],[1,1,1,1]]
k2 = [[0,0,0,0],[0,1,1,0],[0,1,1,0],[0,0,0,0]]


im1 = np.array(plt.imread(pic_1))
im2 = np.array(plt.imread(pic_2))
im3 = np.array(plt.imread(pic_3))

cim1 = ndi.convolve(im1[:,:,0],k0) - im1[:,:,0] +\
       ndi.convolve(im1[:,:,1],k0) - im1[:,:,1] + ndi.convolve(im1[:,:,2],k0) - im1[:,:,2]

cim2 = ndi.convolve(im2[:,:,0],k0) - im2[:,:,0] +\
       ndi.convolve(im2[:,:,1],k0) - im2[:,:,1] + ndi.convolve(im2[:,:,2],k0) - im2[:,:,2]

cim3 = ndi.convolve(im3[:,:,0],k0) - im3[:,:,0] +\
       ndi.convolve(im3[:,:,1],k0) - im3[:,:,1] + ndi.convolve(im3[:,:,2],k0) - im3[:,:,2]

'''
ahmmia.fi
https://www.thedarkweblinks.com/

'''