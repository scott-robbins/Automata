from matplotlib.animation import FFMpegWriter
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import scipy.ndimage as ndi
import numpy as np
import imutils
import time

tic = time.time()


def simulation(state, depth, saveData):
    f = plt.figure()
    simulation = list()
    simulation.append([plt.imshow(state)])
    k0 = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]
    ind2sub = imutils.LIH_flat_map_creator(state)
    '''
        With this model, the actual automata rules can be functionalized, which
        should help me generate tests more rapidly and also hold onto the more 
        interesting rule sets (which often get lost during modification)
    '''
    gen = 0
    while gen <= depth:
        rworld = ndi.convolve(state[:, :, 0], k0, origin=0)
        gworld = ndi.convolve(state[:, :, 1], k0, origin=0)
        bworld = ndi.convolve(state[:, :, 2], k0, origin=0)
        state[:, :, 2] += imutils.draw_centered_box(state[:, :, 0], 10, 1, False)
        state[:, :, 0] += imutils.draw_centered_circle(state[:, :, 0], 15, 0, False)
        for px in range(state.shape[0]*state.shape[1]):
            state = rule_set(ind2sub[px],state,rworld, gworld, bworld, gen, depth)
        simulation.append([plt.imshow(state)])
        gen += 1

    print '\033[1mFINISHED SIMULATION [%ss Elapsed]\n\033[3mRendering...\033[0m' % str(time.time() - tic)
    a = animation.ArtistAnimation(f,simulation,interval=saveData['frame_rate'],blit=True,repeat_delay=500)
    if saveData['save']:
        writer = FFMpegWriter(fps=saveData['fps'], metadata=dict(artist='Me'), bitrate=1800)
        a.save(saveData['file_name'], writer=writer)
    plt.show()
    return state


def rule_set(pos, state, rch, gch, bch, gen, ngen):
    x = pos[0]
    y = pos[1]
    if rch[x, y] % 4 == 0 and (bch[x, y] or gch[x, y])% 6 == 0:
        state[x, y, :] = [1, 1, 1]
    if (rch[x, y] % 5 == 0 and rch[x, y] % 3 == 0) and (bch[x, y] and gch[x, y]) == 0:
        state[x, y, :] = [1, 1, 1]
    if state[x, y, 0] == 1 and state[x, y, 1] == 1 and state[x, y, 2] == 1 and (rch[x,y] or gch[x,y]) % 8 == 0:
        state[x, y, :] = [0, 0, 1]
    if gch[x, y] % 8 == 0 and (bch[x, y] or rch[x, y]) % 8 == 0:
        state[x, y, :] = [0, 0, 0]
    elif state[x, y, 0] == 0 and state[x, y, 1] == 0 and state[x, y, 2] == 0 and rch[x,y] % 4 == 0:
        state[x, y, :] = [1,0,1]
    elif state[x, y, 0] == 1 and state[x, y, 1] == 1 and state[x, y, 2] == 1 and gch[x, y] % 8 == 0:
        state[x, y, :] = [0, 1, 0]

    return state


if __name__ == '__main__':
    ''' DEFINE SIMULATION STATE '''
    width = 120
    height = 120
    state = np.zeros((width, height, 3))
    state[:,:,0] += imutils.draw_centered_circle(state[:,:,0], 55, 1,False)
    state[:,:,0] += imutils.draw_centered_box(state[:, :, 0], 45, 0, False)
    state[:,:,2] += imutils.draw_centered_box(state[:, :, 0], 35, 1, False)
    state[:,:,2] += imutils.draw_centered_box(state[:, :, 0], 25, 0, False)
    state[:,:,2] += imutils.draw_centered_box(state[:, :, 0], 15, 1, False)
    simulation(state, depth=300, saveData={'frame_rate': 150,
                                           'file_name': 'mosaic_6.mp4',
                                           'fps': 40,
                                           'save': True})
