import matplotlib.animation as animation
import matplotlib.pyplot as plt
import scipy.ndimage as ndi
import standard_model
import numpy as np
import imutils
import time
import os

div_0 = [[1,1,0,0,1,1],
         [1,1,0,0,1,1],
         [0,0,1,1,0,0],
         [0,0,1,1,0,0],
         [1,1,0,0,1,1],
         [1,1,0,0,1,1]]

tic = time.time()

width = 250
height = 250
state = np.zeros((width, height))
''' PREPARE UNIVERSE'''
sq_locs = {}
squares = []
n_squares = 100
for s in range(n_squares):
    [x, y] = imutils.spawn_random_point(np.zeros((width, height)))
    if s % 2 ==0:
        obj = standard_model.Organism('square', 0, 4)
    else:
        obj = standard_model.Organism('circle', 0, 4)
    obj.set_position(x, y)
    squares.append(obj)

    sq_locs[s] = [x, y, obj]
    dx = obj.state.shape[0]
    dy = obj.state.shape[1]
    try:
        state[x - int(dx / 2):x + int(dx / 2),
        y - int(dy / 2):y + int(dy / 2)] = obj.state
    except ValueError:
        pass

''' RUN SIMULATION '''
N_Steps = 20
sim = []
f = plt.figure()
sim.append([plt.imshow(state, 'gray')])

field = np.zeros((width, height))
print '[*] Starting Simulation [%ss Elapsed]' % str(time.time()-tic)
points = imutils.LIH_flat_map_creator(np.zeros((width, height)))
for step in range(N_Steps):
    os.system('clear')
    print '[*] Running Simulation [*]'
    for square in squares:
        for mode in square.physics.transition_allocations.keys():
            p = 1 / square.physics.transition_allocations[mode]
            N = np.random.random_integers(0, p, 1)[0]
            n0 = square.mode
            square.mode = N
            square.state = square.reveal(False)
            x = square.x
            y = square.y
            x1 = square.state.shape[0]
            y1 = square.state.shape[1]
            org = sq_locs[2]

            try:
                state[x - int(x1 / 2):x + int(x1 / 2),
                y - int(y1 / 2):y + int(y1 / 2)] = square.state
            except ValueError:
                state[x - int(x1 / 2):x + int(x1 / 2),
                y - int(y1 / 2):y + int(y1 / 2)] = 0

    # TODO Automata ?
    features = ndi.convolve(state,div_0, origin=0)
    ii = 0
    for cell in features.flatten():
        [x,y] = points[ii]
        if cell >= 8 and state[x,y]==0:
            field[x,y] += 1
        if field[x,y] > 10:
            state[x,y] = 1
        ii += 1

    sim.append([plt.imshow(state, 'gray')])
    print '#'*step
print '[*] Simulation Finished [%ss Elapsed]' % str(time.time()-tic)
a = animation.ArtistAnimation(f,sim,interval=300,blit=True, repeat_delay=900)
print '[*[ Rendering Finished [%ss Elapsed]' % str(time.time()-tic)
plt.show()
