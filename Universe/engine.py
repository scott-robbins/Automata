from matplotlib.animation import FFMpegWriter
import matplotlib.animation as animation
import matplotlib.pyplot as plt
from tqdm import tqdm
import scipy.ndimage as ndi
import scipy.misc as misc
import numpy as np
import imutils
import time
import sys
import os

''' 3x3 Kernels '''
k0 = [[1,1,1],[1,0,1],[1,1,1]]
k1 = [[0,1,0],[1,0,1],[0,1,0]]
k2 = [[0,0,0],[1,1,1],[0,0,0]]
k3 = [[1,1,1],[0,0,0],[1,1,1]]

''' 5x5 Kernels '''
f1 = [[1,0,1,0,1],
      [0,1,1,1,0],
      [1,1,0,1,1],
      [0,1,1,1,0],
      [1,0,1,0,1]]

f2 = [[1,1,1,1,1],
      [1,0,0,0,1],
      [1,0,1,0,1],
      [1,0,0,0,1],
      [1,1,1,1,1]]


ani_cmd = 'ffmpeg -r 20 -f image2 -i img%d.png -vcodec libx264 -pix_fmt yuv420p simulation.mp4;clear'


def miniverse(state, depth, save):
    print '\033[1mRUNNING \033[31mSIMULATION\033[0m'
    t0 = time.time()
    bar = tqdm(total=depth)
    # f = plt.figure()
    # film = []
    # film.append(state)
    for step in tqdm(range(depth)):
        rch = state[:,:,0]
        gch = state[:,:,1]
        bch = state[:,:,2]

        cmb = ndi.convolve(bch, k0, origin=0)
        cmg = ndi.convolve(gch, k0, origin=0)

        ind2sub = imutils.LIH_flat_map_creator(state[:,:,0])
        for ii in range(state.shape[0]*state.shape[1]):
            flip = np.random.random_integers(0,1,1)[0]
            [x, y] = ind2sub[ii]
            if 8 > cmb[x,y]> 1 and cmb[x,y] % 4==0:
                if flip:
                    state[x,y,1] -= 1
            if 0 < cmb[x,y] < cmg[x,y] >= 4:
                state[x,y,1] = 0
                state[x,y,0] = 1
            if rch[x,y] and cmb[x,y] < 6:
                state[x,y,0] = 1
        misc.imsave('img%d.png'%step, np.array(state).astype(np.uint8))
        # film.append([plt.imshow(state)])
        # if flip and step %10==0:
        #     world[:, :, 2] += np.random.random_integers(-10, 10, w * h).reshape((w, h))
        bar.update(1)
    # a = animation.ArtistAnimation(f,film,interval=100,blit=True,repeat_delay=900)
    print 'Simulation FINISHED [%ss Elapsed]' % str(time.time()-t0)
    bar.close()
    os.system(ani_cmd)
    os.system('vlc %s' % 'test.mp4')


def simulation_two(state, depth, save):
    print '\033[1mRUNNING \033[31mSIMULATION\033[0m'
    f = plt.figure()
    reel = []
    reel.append([plt.imshow(state)])
    t0 = time.time()
    bar = tqdm(total=depth)
    for step in tqdm(range(depth)):
        rch = state[:, :, 0]
        gch = state[:, :, 1]
        bch = state[:, :, 2]

        cmb = ndi.convolve(bch, k0, origin=0)
        cmg = ndi.convolve(gch, k0, origin=0)
        cmr = ndi.convolve(rch, k0, origin=0)
        ind2sub = imutils.LIH_flat_map_creator(state[:,:,0])

        chance = np.random.random_integers(0,1,1)[0]

        for jj in range(state.shape[0]*state.shape[1]):
            [x, y] = ind2sub[jj]
            if cmb[x,y] == 8 or cmb[x,y]%8==0:
                state[x,y,0] = 0
                state[x,y,1] = 1
                state[x,y,2] = 1
            if cmb[x,y] == 3 and cmg[x,y] == 3:
                state[x,y,0] = 1
            if 0 < cmb[x,y] < cmg[x,y] >= 4:
                state[x,y,1] = 0
                state[x,y,0] = 1
            if 0 < cmg[x,y] < cmb[x,y] < 7 and cmb[x,y] > 4:
                state[x,y,:] = 1
            if gch[x,y] and cmb[x,y] < 6 and cmg[x,y]%5==0:
                if chance:
                    state[x,y,0] = 1
                else:
                    state[x,y,0] = 0
            if rch[x,y] and gch[x,y] and bch[x,y] and chance:
                if cmg[x, y] > (cmr[x, y] and cmb[x, y]):
                    mutation = np.random.random_integers(0, 1, 12).reshape((2,2,3))
                    try:
                        state[x-1:x+1, y-1:y+1, :] = mutation
                    except:
                        pass
        reel.append([plt.imshow(state)])
        bar.update(1)
    a = animation.ArtistAnimation(f, reel, interval=100, blit=True, repeat_delay=900)
    print 'Simulation FINISHED [%ss Elapsed]' % str(time.time() - t0)
    bar.close()
    if save['save']:
        writer = FFMpegWriter(fps=save['frame_rate'], metadata=dict(artist='Me'), bitrate=1800)
        a.save(save['file_name'], writer=writer)
    plt.show()


# ########################################## MAIN ####################################### #
if __name__ == '__main__':
    w = 250
    h = 250
    depth = 100
    world = np.zeros((w, h, 3))
    world[:, :, 2] += np.random.random_integers(0, 1, w * h).reshape((w, h))

    ''' _________ MODEL _____________
       |------>----||------<----|    |
     {St[0]}     {St[1]}    {St[2]}  | 
       |------<----|------>----|     |
      / \         / \         / \    |
     /   \       /   \       /   \   |_____________
    E0+  E0-   E1+   E1-    E2+  E2-        Events | 
    '''

    simulation_two(world,depth, {'save':True, 'frame_rate': 20, 'file_name': 'typeA.mp4'})
    # os.system('ls *png | while read n; do rm $n; done')
