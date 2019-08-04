from matplotlib.animation import FFMpegWriter
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import scipy.ndimage as ndi
import numpy as np
import imutils
import time
import sys

TIC = time.time()


class ColorParticleSimulator:
    width = 0
    height = 0
    state = np.array((width,height))
    dims = []
    n_particles = 0
    n_red = 0
    n_blue = 0
    n_green = 0
    n_cyan = 0
    n_magenta = 0
    n_white = 0
    frame_rate = 0
    points = {'red'  :[],
              'green':[],
              'blue' :[]}

    def __init__(self, configuration):
        self.initialize(configuration)
        self.simulate(30)

    def initialize(self, config):
        tic = time.time()
        self.dims = [config['width'], config['height'], 3]
        self.state = np.zeros(self.dims)
        slate = np.zeros((self.dims[0], self.dims[1]))
        if config['n_red'] >0:
            for rpt in range(config['n_red']):
                [x,y] = imutils.spawn_random_point(slate)
                try:
                    self.state[x, y, :] = [1, 0, 0]
                    self.n_red += 1
                except IndexError:
                    pass
        if config['n_green'] > 0:
            for gpt in range(config['n_green']):
                [x, y] = imutils.spawn_random_point(slate)
                try:
                    self.state[x,y,:] = [0,1,0]
                    self.n_green += 1
                except IndexError:
                    pass
        if config['n_blue'] > 0:
            for bpt in range(config['n_blue']):
                [x, y] = imutils.spawn_random_point(slate)
                try:
                    self.state[x,y,:] = [0,0,1]
                    self.n_blue += 1
                except IndexError:
                    pass
        print '\033[1m\033[31m%d \033[0m\033[1mRed Particles Added To Simulation\033[0m' % self.n_red
        print '\033[1m\033[32m%d \033[0m\033[1mGreen Particles Added To Simulation\033[0m' % self.n_green
        print '\033[1m\033[34m%d \033[0m\033[1mBlue Particles Added To Simulation\033[0m' % self.n_blue

        # Q3R = 0
        # Q3G = 0
        # Q3B = 0
        #
        # Q4R = 0
        # Q4G = 0
        # Q4B = 0
        self.frame_rate = config['frame_rate']
        points = imutils.LIH_flat_map_creator(slate)
        # TODO: Count all particles for simulation
        for i in range(len(slate.flatten())-1):
            [x,y] = points[i]
            pixel = self.state[x,y,:]
            if pixel[0]==1 and pixel[1]==0 and pixel[2]==0:
                self.points['red'].append([x, y])
            if pixel[0]==0 and pixel[1]==1 and pixel[2]==0:
                self.points['green'].append([x, y])
            if pixel[0]==0 and pixel[1]==0 and pixel[2]==1:
                self.points['blue'].append([x, y])
        # print '%d Red Pixels in Quadrant 2' % Q2R
        # print '%d Green Pixels in Quadrant 2' % Q2G
        # print '%d Blue Pixels in Quadrant 2' % Q2B
        print '%d Red Particles Found... ' % len(self.points['red'])
        print '%d Green Particles Found... ' % len(self.points['green'])
        print '%d Blue Particles Found... ' % len(self.points['blue'])
        print '\033[1m\033[3m[%ss Elapsed]\033[0m' % str(time.time()-tic)

    def simulate(self, depth):
        f = plt.figure()
        simulation = []
        k0 = [[1,1,1],[1,1,1],[1,1,1]]
        for step in range(depth):
            state = self.state
            for rpt in self.points['red']:
                red_move = np.random.random_integers(1,9,1)[0]
                rm = {1: [rpt[0] - 1, rpt[0] - 1], 2: [rpt[0], rpt[1] - 1], 3: [rpt[0] + 1, rpt[1] - 1],
                      4: [rpt[0] - 1, rpt[1]], 5: rpt, 6: [rpt[0] + 1, rpt[1]],
                      7: [rpt[0] - 1, rpt[1] + 1], 8: [rpt[0], rpt[1] + 1], 9: [rpt[0] + 1, rpt[1] + 1]}
                rmv = rm[red_move]
                state[rpt[0], rpt[1], :] = [0, 0, 0]
                try:
                    state[rmv[0], rmv[1], :, ] = [1, 0, 0]
                except IndexError:
                    pass
            for gpt in self.points['green']:
                gm = {1: [gpt[0] - 1, gpt[0] - 1], 2: [gpt[0], gpt[1] - 1], 3: [gpt[0] + 1, gpt[1] - 1],
                      4: [gpt[0] - 1, gpt[1]], 5: gpt, 6: [gpt[0] + 1, gpt[1]],
                      7: [gpt[0] - 1, gpt[1] + 1], 8: [gpt[0], gpt[1] + 1], 9: [gpt[0] + 1, gpt[1] + 1]}
                green_move = np.random.random_integers(1,9,1)[0]
                gmv = gm[green_move]
                state[bpt[0], bpt[1], :] = [0, 0, 0]
                try:
                    state[gmv[0], gmv[1], :, ] = [0, 1, 0]
                except IndexError:
                    pass
            for bpt in self.points['blue']:
                bm = {1:[bpt[0]-1,bpt[0]-1], 2:[bpt[0],bpt[1]-1], 3:[bpt[0]+1,bpt[1]-1],
                      4:[bpt[0]-1,bpt[1]], 5: bpt, 6:[bpt[0]+1, bpt[1]],
                      7:[bpt[0]-1,bpt[1]+1], 8:[bpt[0],bpt[1]+1], 9:[bpt[0]+1,bpt[1]+1]}
                blue_move = np.random.random_integers(1,9,1)[0]
                bmv = bm[blue_move]
                state[bpt[1], bpt[0], :] = [0, 0, 0]
                try:
                    state[bmv[1], bmv[0], :, ] = [0, 0, 1]
                except IndexError:
                    pass
            # NOW for each step iterate through each pixel
            #  and apply cellular automata rules
            ind2sub = imutils.LIH_flat_map_creator(np.zeros((self.dims[0], self.dims[1])))
            rch = ndi.convolve(self.state[:, :, 0], k0)
            gch = ndi.convolve(self.state[:, :, 1], k0)
            bch = ndi.convolve(self.state[:, :, 2], k0)
            for point in range(self.dims[0]*self.dims[1]):
                [x, y] = ind2sub[point]
                self.apply_rules([x,y],rch,gch,bch)
            self.state = state
            simulation.append([plt.imshow(self.state)])
        print '%d Frame Simulation Finished [%ss Elapsed]\nRendering...' % (depth,str(time.time() - TIC))
        a = animation.ArtistAnimation(f, simulation, self.frame_rate,blit=True,repeat_delay=900)
        # TODO: Add saving
        plt.show()

    def apply_rules(self, pos, rch, gch, bch):
        x = pos[0]
        y = pos[1]
        if self.state[x, y, 0] == 0 and self.state[x, y, 1] == 0 and self.state[x, y, 2] == 0:  # BLACK
            if rch[x,y] ==9 and bch[x,y]==0:
                self.state[x,y,:] = [1,0,0]
            if (rch[x,y] and bch[x,y]) == 8:
                self.state[x,y,:] = [1,0,1]
        elif self.state[x,y,0]==1 and self.state[x,y,1]==0 and self.state[x,y,2]==0: # RED
            if rch[x,y] > 4:
                self.state[x,y,:] = [0,0,0]
        elif self.state[x, y, 0] == 0 and self.state[x, y, 1] == 0 and self.state[x, y, 2] == 1:  # BLUE
            if rch[x,y] > 4:
                self.state[x,y,:] = [0,0,0]


if __name__ == '__main__':
    config = {'width' : 100,
              'height': 100,
              'n_particles': 150,
              'n_red': 50,
              'n_blue': 50,
              'n_green':0,
              'frame_rate': 200}

    CA_cps = ColorParticleSimulator(config)
