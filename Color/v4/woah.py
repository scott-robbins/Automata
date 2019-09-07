from matplotlib.animation import FFMpegWriter
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import scipy.ndimage as ndi
import scipy.misc as misc
import numpy as np
import imutils
import time
import os

# TODO: ASCII Art Splash while things load up

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


def pre_process(image_path, show):
    im = np.array(plt.imread(image_path))
    dims = im.shape
    minima = im.min()
    maxima = im.max()
    mean = im.mean()
    std = im.std()
    meanie = ndi.gaussian_laplace(im-im.mean(), sigma=.1)
    stats = [dims, minima, maxima, mean, std]
    if show:
        print '=== Loaded: %s ===' % image_path
        print 'Shape: %s' % str(dims)
        print 'Min: %s' % str(minima)
        print 'Max: %s' % str(maxima)
        print 'Mean: %s' % str(mean)
        print 'Std: %s' % str(std)
        f, ax = plt.subplots(2, 2)
        ax[0,0].imshow(im)
        ax[0,1].imshow(meanie)
        ax[1,0].imshow(ndi.convolve(meanie[:,:,0], k0))
        ax[1,1].imshow(ndi.convolve(im[:,:,1]-meanie[:,:,0]+im[:,:,2], k1))
        plt.show()
    return stats, meanie


def processor(im, mode, depth):
    progress = ''
    print '##### RUNNING SIMULATION #####'
    f = plt.figure()
    im = np.array(im)
    simulation = []
    ii = 0
    mapping = imutils.LIH_flat_map_creator(im)
    for step in range(depth):
        progress += '#' * int(2*step/float(depth))
        print progress
        rch = im[:, :, 0]
        gch = im[:, :, 1]
        bch = im[:, :, 0]

        rc1 = ndi.convolve(rch,k0)
        gc1 = ndi.convolve(gch,k0)
        bc1 = ndi.convolve(bch,k0)

        rc2 = ndi.convolve(rch,k1)
        gc2 = ndi.convolve(gch,k1)
        bc2 = ndi.convolve(bch,k1)
        rmean1 = rc1.mean()
        rmean2 = rc2.mean()
        gmean1 = gc1.mean()
        gmean2 = gc2.mean()
        bmean1 = bc1.mean()
        bmean2 = bc2.mean()

        rc1 -= rmean1
        rc2 -= rmean2
        gc1 -= gmean1
        gc2 -= gmean2
        bc1 -= bmean1
        bc2 -= bmean2

        im[:,:,0] = (rc1 + rc2)/2
        im[:,:,1] = (gc1 + gc2)/2
        im[:,:,2] = (bc1 + bc2)/2

        for pt in range(im.shape[0]*im.shape[1]):
            [x,y] = mapping[pt]
            if gch[x,y] % 6==0 and gc1[x,y]>=gmean1:
                im[x,y,1] += 1
            if rch[x,y] and rc1[x,y]>rmean1 and rc2[x,y]>rmean2:
                im[x,y,0] += 1
            if mode == 0:
                if rc1[x, y] >= rmean1:
                    im[x, y, 0] -= 1
                if rch[x, y] % 3 == 0 and rc2[x, y] >= rmean2:
                    im[x, y, 0] == 0
                if bch[x, y] % 2 == 0 and bc2[x, y] >= bmean1:
                    im[x, y, 2] -= 1

        # misc.imsave('img'+str(ii)+'.png', im-im.mean())
        simulation.append([plt.imshow(im)])
        ii += 1

    print 'FINISHED [%ss Elapsed]' % str(time.time() - tic)
    a = animation.ArtistAnimation(f,simulation,interval=100,blit=True,repeat_delay=900)
    # writer = FFMpegWriter(fps=12, metadata=dict(artist='Me'), bitrate=1800)
    # a.save('earth.mp4', writer=writer)
    plt.show()


istat1, mim1 = pre_process(pic_1, 0)
istat2, mim2 = pre_process(pic_2, 0)
istat3, mim3 = pre_process(pic_3, 0)

processor(mim2, 130, 0)
print 'SAVING FRAMES [%ss Elapsed]' % str(time.time()-tic)
# os.system(ani_cmd)
# os.system('vlc %s' % file_name_out)
# s.system(clean)
