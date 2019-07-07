from matplotlib.animation import FFMpegWriter
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import scipy.ndimage as ndi
import numpy as np
import imutils
import time
import sys

tic = time.time()

R = [1,0,0]
G = [0,1,0]
B = [0,0,1]

def create_color_pt_cloud(state, color, n_points):
    for i in range(n_points):
        [x, y] = imutils.spawn_random_point(np.zeros((width, height)))
        if color == 'R':
            state[x,y,0] = 1
        if color == 'G':
            state[x,y,1] = 1
        if color == 'B':
            state[x,y,2] = 1
    return state


def rule_set_one(pos, state, rch, gch, bch):
    x = pos[0]
    y = pos[1]

    m1 = 6  # MOD: Organizer
    m2 = 5  # MOD: Chaos (Inverts Behavior of Organization)

    if state[x,y,0]==1 and state[x,y,1]==0 and state[x,y,2] == 0:   # RED
        if rch[x,y] % m1 == 0:
            state[x,y,:] = [1,0,1]
        if gch[x,y] % m2 == 0:
            state[x,y,:] = [0,1,1]
    elif state[x,y,0]==0 and state[x,y,1]==1 and state[x,y,2] == 0:   # GREEN
        if gch[x,y] % m1 == 0:
            state[x,y,:] = [1,1,0]
        if rch[x,y] % m2 == 0:
            state[x,y,:] = [1,0,1]
    elif state[x,y,0]==0 and state[x,y,1]==0 and state[x,y,2] == 1:   # BLUE
        if bch[x,y] % m1 == 0:
            state[x,y,:] = [0,1,1]
        if gch[x,y] % m2 == 0:
            state[x,y,:] = [0,1,0]
    # TODO: K,W
    elif state[x, y, 0] == 0 and state[x, y, 1] == 1 and state[x, y, 2] == 1:  # CYAN
        if rch[x,y] % m1 == 0:
            state[x,y,:] = [1,0,1]
        if gch[x,y] % m2 == 0:
            state[x,y,:] = [0,1,0]
        if bch[x,y] % m2 == 0:
            state[x,y,:] = [0,0,1]
    elif state[x,y,0] == 1 and state[x,y,1] == 0 and state[x,y,2] == 1:  # MAGENTA
        if rch[x,y] % m2 == 0:
            state[x,y,:] = [1,0,0]
        if gch[x,y] % m2 == 0:
            state[x,y,:] = [0,1,1]
        if bch[x,y] % m1 == 0:
            state[x,y,:] = [0,0,1]
    elif state[x,y,0]==1 and state[x,y,1]==1 and state[x,y,2] == 0:       # YELLOW
        if rch[x,y] % m1 == 0:
            state[x,y, :] = [0,0,1]
        if rch[x,y] % m2 == 0:
            state[x,y, :] = [1,0,0]
        if gch[x,y] % m1 == 0:
            state[x,y, :] = [0,1,0]
        if gch[x,y] % m2==0:
            state[x,y,:] = [1,0,0]
        if bch[x,y] % m1==0:
            state[x,y,:] = [1,1,1]
        if bch[x,y] % m2==0:
            state[x,y,:] = [0,1,1]
    return state


def rule_set_two(pos,state,rch,gch,bch,gen):
    x = pos[0]
    y = pos[1]

    m1 = 7
    m2 = 8

    if gch[x,y] % m1 == 0:
        state[x,y,:] = [0,1,0]
    if gch[x,y] % m2 == 0:
        state[x,y,:] = [0,1,1]
    if bch[x,y] % m1 == 0:
        state[x,y,:] = [0,0,1]
    if bch[x,y] % m2 == 0:
        state[x,y,:] = [1,0,1]
    if rch[x,y] % m1 == 0:
        state[x,y,:] = [1,0,0]
    if rch[x,y] % m2 == 0:
        state[x,y,:] = [1,1,0]
    if (rch[x,y] and bch[x,y]) % m1 == 0:
        state[x,y,:] = [0,1,1]
    elif (gch[x,y] and rch[x,y]) % m1 == 0:
        state[x,y,:] = [1,1,0]
    # if gen > 10 and gch[x,y] == 8:
    #     state[x,y,:] = [0,1,0]

    return state


def simulation(state, depth, saveData):
    f = plt.figure()
    simulation = list()
    simulation.append([plt.imshow(state)])

    k0 = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]
    ind2sub = imutils.LIH_flat_map_creator(state)

    gen = 0
    while gen <= depth:
        rworld = ndi.convolve(state[:, :, 0], k0, origin=0)
        gworld = ndi.convolve(state[:, :, 1], k0, origin=0)
        bworld = ndi.convolve(state[:, :, 2], k0, origin=0)

        for px in range(state.shape[0]*state.shape[1]):
            #state = rule_set_one(ind2sub[px], state, rworld, gworld, bworld)
            state = rule_set_two(ind2sub[px], state, rworld, gworld, bworld, gen)
        simulation.append([plt.imshow(state)])
        gen += 1

    print 'FINISHED [%ss Elapsed]' % str(time.time() - tic)
    a = animation.ArtistAnimation(f,simulation,interval=saveData['frame_rate'],blit=True,repeat_delay=500)
    if saveData['save']:
        writer = FFMpegWriter(fps=saveData['frame_rate'], metadata=dict(artist='Me'), bitrate=1800)
        a.save(saveData['file_name'], writer=writer)
    plt.show()


if __name__ == '__main__':
    ''' DEFINE SIMULATION STATE '''
    width = 100
    height = 100
    state = np.zeros((width, height, 3))
    state[:,:,0] += imutils.draw_centered_circle(np.zeros((width,height)), width/4,1,False)
    state[:,:,2] += imutils.draw_centered_box(np.zeros((width, height)), width-60,1,False)

    if 'gas' in sys.argv:
        try:
            state = create_color_pt_cloud(state, sys.argv[2], int(sys.argv[3]))
        except:
            print 'Incorrect Usage!'
            pass

    ''' Optionally load image as initial state'''
    if '-i' in sys.argv:
        state = np.array(plt.imread(sys.argv[2]))

    print '\033[1m\033[3m** STARTING SIMULATION **\033[0m'
    ''' RUN SIMULATION '''
    simulation(state, 50, {'save': True,
                           'frame_rate': 10,
                           'file_name': 'CA_organisms2.mp4'})
# EOF
