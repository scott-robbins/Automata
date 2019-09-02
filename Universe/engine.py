import matplotlib.animation as animation
import matplotlib.pyplot as plt
import standard_model
import numpy as np
import imutils


width = 250
height = 250
state = np.zeros((width, height))
''' PREPARE UNIVERSE'''
sq_locs = {}
squares = []
n_squares = 30
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
N_Steps = 30
sim = []
f = plt.figure()
sim.append([plt.imshow(state, 'gray')])
for step in range(N_Steps):
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

    sim.append([plt.imshow(state, 'gray')])
a = animation.ArtistAnimation(f,sim,interval=100,blit=True, repeat_delay=900)
plt.show()
