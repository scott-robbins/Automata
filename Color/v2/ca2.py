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
        try:
            if color == 'R':
                state[x, y, 0] = 1
            if color == 'G':
                state[x, y, 1] = 1
            if color == 'B':
                state[x, y, 2] = 1
            if color == 'C':
                state[x, y, :] = [0, 1, 1]
            if color == 'M':
                state[x, y, :] = [1, 0, 1]
            if color == 'Y':
                state[x, y, :] = [1, 1, 0]
            if color == 'K':
                state[x, y, :] = [0, 0, 0]
            if color == 'W':
                state[x, y, :] = [1, 1, 1]
        except IndexError:
            pass
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


def rule_set_two(pos,state,rch,gch,bch,gen,ngen):
    x = pos[0]
    y = pos[1]

    m1 = 7
    m2 = 8

    red = False
    green = False
    blue = False
    cyan = False
    magenta = False
    yellow = False
    black = False
    white = True

    if gch[x,y] % m1 == 0 and gen < ngen/2:
        state[x,y,:] = [0,1,0]
    elif gch[x,y] % m2 == 0:
        state[x,y,:] = [0,1,1]
    if gch[x,y] % m2 == 0:
        state[x,y,:] = [0,1,1]
    if bch[x,y] % m1 == 0:
        state[x,y,:] = [0,0,1]
    if bch[x,y] % m2 == 0:
        state[x,y,:] = [1,0,1]
    if rch[x,y] % m1 == 0 and gen < ngen/2:
        state[x,y,:] = [1,0,0]
    elif rch[x,y] % m1 == 0:
        state[x,y,:] = [1,0,1]
    if rch[x,y] % m2 == 0:
        state[x,y,:] = [1,1,0]
    if (rch[x,y] and bch[x,y]) % m1 == 0:
        state[x,y,:] = [0,1,1]
    elif (gch[x,y] and rch[x,y]) % m1 == 0:
        state[x,y,:] = [1,1,0]
    if (float(gen)/ngen) >= 0.5: # Constraining Growth of Organism
        if gch[x,y] == 8 and (rch[x,y] and bch[x,y]) % m1 != 0:
         state[x,y,:] = [1,0,0]

        if state[x,y,0]==1 and state[x,y,1]==1 and state[x,y,2]==0: # YELLOW
            yellow = True
            if bch[x, y] % m2 == 0:
                state[x,y,:] = [0,0,1]
            if bch[x, y] % m1 == 0:
                state[x,y,:] = [1,0,1]
            if (rch[x,y] and gch[x,y]) % (m1 or m2) ==0:
                state[x,y,:] = [0,1,1]
        # Constrain overgrowth
        if red or yellow and gch[x, y] <= rch[x,y]:
            state[x,y,:] = [0,1,0]

        if state[x,y,0] == 0 and state[x,y,1] == 0 and state[x,y,2] == 1:   # BLUE
            blue = True
            if rch[x,y] > (gch[x,y] or bch[x,y]):
                state[x,y,:] = [1,0,0]
            if gch[x,y] > (rch[x,y] or bch[x,y]):
                state[x,y,:] = [0,1,0]
            if bch[x,y] > (rch[x,y] and gch[x,y]):
                state[x,y,:] = [1,1,1]
            if rch[x,y] == gch[x,y] :
                state[x,y,:] = [1,1,0]

        if state[x, y, 0] == 0 and state[x, y, 1] == 1 and state[x, y, 2] == 0: # GREEN
            green = True
            if bch[x,y] > 1 and gch[x,y] % 8 == 0:
                state[x,y,:] = [0,0,1]
            if bch[x, y] == gch[x, y] or bch[x,y]%m2==0:
                state[x, y, :] = [0, 1, 1]
            if gch[x,y] == 8 and rch[x,y]%m2==0:
                state[x,y,:] = [1,0,0]
        if state[x,y,0] == 1 and state[x,y,1] == 0 and state[x,y,2] == 0: # RED
            red = True
            if rch[x,y] % 3 == 0:
                if bch[x,y] > gch[x,y]:
                    state[x,y,:] = [0,0,1]
                if bch[x, y] == gch[x, y] or bch[x,y]%m2==0:
                   state[x,y,:] = [0,1,1]
                if rch[x,y] == 8 and gch[x,y] % m1==0:
                    state[x,y,:] = [1,1,0]

        if bch[x, y] % m1 == 0:
            state[x, y, :] = [1, 0, 1]
        if rch[x, y] % m2 == 0:
            state[x, y, :] = [1, 0, 1]
        if rch[x, y] % m1 == 0:
            state[x, y, :] = [0, 1, 1]

    return state


def rule_set_tre(pos, state, rch, gch, bch, gen, ngen):
    x = pos[0]
    y = pos[1]

    ravg = rch.mean()
    gavg = gch.mean()
    bavg = bch.mean()

    m1 = 7
    m2 = 8

    red = False
    green = False
    blue = False
    cyan = False
    magenta = False
    yellow = False
    black = False
    white = True

    if state[x, y, 0] == 1 and state[x, y, 1] == 0 and state[x, y, 2] == 0:
        red = True
    elif state[x, y, 0] == 0 and state[x, y, 1] == 1 and state[x, y, 2] == 0:
        green = True
    elif state[x, y, 0] == 0 and state[x, y, 1] == 0 and state[x, y, 2] == 1:
        blue = True
    elif state[x, y, 0] == 0 and state[x, y, 1] == 1 and state[x, y, 2] == 1:
        cyan = True
    elif state[x, y, 0] == 1 and state[x, y, 1] == 0 and state[x, y, 2] == 1:
        magenta = True
    elif state[x, y, 0] == 1 and state[x, y, 1] == 1 and state[x, y, 2] == 0:
        yellow = True
    if (red and rch[x, y] > ravg) or (blue and bch[x, y] > bavg) and not yellow:
        state[x, y] = [1, 0, 1]
    if magenta and (gch[x, y] >= gavg and rch[x,y] >= ravg and bch[x,y] >= bavg):
        state[x, y] = [0, 1, 0]

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
            '''
            With this model, the actual automata rules can be functionalized, which
            should help me generate tests more rapidly and also hold onto the more 
            interesting rule sets (which often get lost during modification)
            '''
            # state = rule_set_one(ind2sub[px], state, rworld, gworld, bworld)
            # state = rule_set_two(ind2sub[px], state, rworld, gworld, bworld, gen, depth)
            state = rule_set_tre(ind2sub[px], state, rworld, gworld, bworld, gen, depth)
        simulation.append([plt.imshow(state)])
        gen += 1

    print 'FINISHED [%ss Elapsed]' % str(time.time() - tic)
    a = animation.ArtistAnimation(f,simulation,interval=saveData['frame_rate'],blit=True,repeat_delay=500)
    if saveData['save']:
        writer = FFMpegWriter(fps=saveData['frame_rate'], metadata=dict(artist='Me'), bitrate=1800)
        a.save(saveData['file_name'], writer=writer)
    plt.show()
    return state


if __name__ == '__main__':
    ''' DEFINE SIMULATION STATE '''
    width = 100
    height = 100
    state = np.zeros((width, height, 3))
    state[:, :, 0] += imutils.draw_centered_box(np.zeros((width, height)), 45, 1, False)
    state[:, :, 1] += imutils.draw_centered_circle(np.zeros((width, height)), 35, 1, False)
    state[:, :, 2] += imutils.draw_centered_box(np.zeros((width, height)), 35, 1, False)

    if 'gas' in sys.argv:
        state = np.zeros((width, height, 3))
        state[0: 30, 0: 30] += create_color_pt_cloud(state[0:30, 0:30], 'R', 1000)
        state[40:70, 10:40] += create_color_pt_cloud(state[20:50,10:40], 'B', 1000)
    ''' Optionally load image as initial state'''
    if '-i' in sys.argv:
        state = np.array(plt.imread(sys.argv[2]))

    print '\033[1m\033[3m** STARTING SIMULATION **\033[0m'
    ''' RUN SIMULATION '''
    state = simulation(state, 70, {'save': True,
                           'frame_rate': 10,
                           'file_name': 'CA_2.mp4'})
# EOF
