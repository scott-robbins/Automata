from matplotlib.animation import FFMpegWriter
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import scipy.ndimage as ndi
import numpy as np
import imutils
import time
import sys


def growth_simulate(state, n_steps, doSave):
    t0 = time.time()
    f = plt.figure()
    history = [state]
    simulation = list()
    simulation.append([plt.imshow(state, 'gray')])
    for i in range(n_steps):
        world = ndi.convolve(state, np.ones((3, 3)))
        avg = world.mean()
        for x in range(state.shape[0]):
            for y in range(state.shape[1]):
                if world[x, y] % 5 and world[x,y] >= avg:
                    state[x, y] = 1
                    world[x,y] = 1
                if world[x, y] == 8 and state[x,y] == 0:
                    state[x,y] = -1
                    world[x,y] = 1
                if world[x, y] % 3 == 0 and state[x,y]>=1:
                    state[x, y] -= 1
                    world[x,y] = 1
                if state[x,y] > 15 and (world[x,y] == 8 or world[x,y] == 6):
                    state[x,y] = 0
        simulation.append([plt.imshow(state, 'gray')])
        history.append(state)
    print '\033[31m\033[1m\t\t** SIMULATION FINISHED [%ss Elapsed]\033[0m\033[1m **\033[0m' % \
          str(time.time()-t0)
    print '\033[3mRendering %d Frames\033[0m' % len(simulation)
    a = animation.ArtistAnimation(f, simulation, interval=100,blit=True, repeat_delay=900)
    if doSave['do']:
        writer = FFMpegWriter(fps=doSave['fps'], metadata=dict(artist='Me'), bitrate=1800)
        a.save(doSave['name'], writer=writer)
    plt.show()
    return history


def big_bang(state, n_steps, doSave):
    f = plt.figure()
    t0 = time.time()
    history = [state]
    simulation = list()
    simulation.append([plt.imshow(state, 'gray')])
    for i in range(n_steps):
        world = ndi.convolve(state, np.ones((3, 3)))
        avg = world.mean()
        depth = np.array(state).max()
        mavg = np.array(state).mean()
        for x in range(state.shape[0]):
            for y in range(state.shape[1]):
                if world[x, y] % 3 and world[x, y] > avg:
                    state[x, y] -= 1
                    world[x, y] = 1
                if world[x, y] == 8 and world[x, y] <= avg:
                    state[x, y] += 1
                    world[x, y] = 1
                if (state[x, y] % 5 == 0 or state[x, y] == mavg) and world[x, y] % 7 == 0:
                    state[x, y] = 0
                if depth-depth/5<state[x,y] <= depth or state[x,y] == mavg:
                    state[x,y] = 1
        simulation.append([plt.imshow(state, 'gray')])
        history.append(state)
    print '\033[31m\033[1m\t\t** SIMULATION FINISHED [%ss Elapsed]\033[0m\033[1m **\033[0m' % \
          str(time.time()-t0)
    print '\033[3mRendering %d Frames\033[0m' % len(simulation)
    a = animation.ArtistAnimation(f, simulation, interval=100,blit=True, repeat_delay=900)
    if doSave['do']:
        writer = FFMpegWriter(fps=doSave['fps'], metadata=dict(artist='Me'), bitrate=1800)
        a.save(doSave['name'], writer=writer)
    plt.show()
    return history


def initialize():
    print '\033[1m=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=\n'\
            '||                        _______________________                           ||\n'\
            '||                       /=-=-~:-MMMMMMMMM-:~-=-=\                           ||\n'\
            '||                       |XXXmmMMMMMMMMMMMMMmmXXX|                          ||\n'\
            '||                       |__ <\033[31mA.U.T.O.M.A.T.A\033[0m\033[1m> __           ||\n'\
            '||                       |XXXwwWWWWWWWWWWWWWwwXXX|                          ||\n'\
            '||                       \=-=-~:_VVVVVVVV_:~-=-=-/                           ||\n'\
                '=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=~=\n'
    ''' DEFINE DIMENISONS'''
    w = 250
    h = 250
    state = np.zeros((w, h))
    ''' CREATE INITIAL STATE '''
    state = imutils.draw_centered_circle(state, 120, 2, False)
    state = imutils.draw_centered_circle(state, 60, 2, False)
    state = imutils.draw_centered_box(state, 20, 0, False)
    state = imutils.draw_centered_box(state, 80, 1, False)
    state = imutils.draw_centered_circle(state, 40, 2, False)

    state_2 = np.zeros((w, h))
    state_2 = imutils.draw_centered_box(state, 60, 2, False)
    state_2 = imutils.draw_centered_circle(state, 80, 1, False)
    state_2 += np.random.random_integers(-1, 2, w * h).reshape((w, h))
    return state, state_2


def main():
    state, state_2 = initialize()
    plt.imshow(state, 'gray')
    plt.close()

    if len(sys.argv) == 3:
        state_2 = np.array(plt.imread(sys.argv[2]))[:, :, 0]

    if len(sys.argv) > 1:
        print '\033[1m\033[36m\t\tSTARTING ' + str(sys.argv[1]).upper() + \
              ' SIMULATION\033[0m\t\033[1m[Image Shape: (%d,%d)]' % (state_2.shape[0], state_2.shape[1])
        ''' SELECT A SIMULATION '''
    if 'growth' in sys.argv:
        save = {'do': False,
                'name': 'growth.mp4',
                'fps': 55}
        sim = growth_simulate(state, 350, save)
    if 'big_bang' in sys.argv:
        save = {'do': False,
                'name': 'big_steal.mp4',
                'fps': 65}
        sim = big_bang(state_2, 150, save)


if __name__ == '__main__':
    main()

