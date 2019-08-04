import matplotlib.pyplot as plt
import scipy.ndimage as ndi
import numpy as np
import imutils
import os


'''
define value for a transition from one 
value to other (defined by row,col)

(0,0)__________________(16,0)
  |                       |
  |                       |
  |                       |
(0,16)__________________(16,16) '''

LUT = np.zeros((16, 16))
example_state = np.random.random_integers(0,15,36).reshape((6, 6))
example_goal = np.random.random_integers(0,15,36).reshape((6, 6))

f, ax = plt.subplots(1, 2)
ax[0].imshow(example_state, 'gray')
ax[1].imshow(example_goal, 'gray')
plt.show()

# TODO: Using a LUT, automate ability to go from example to goal
transition_matrix = example_goal-example_state
print 'Max: %s' % str(np.array(transition_matrix).max())
print 'Min: %s' % str(np.array(transition_matrix).min())
print 'Mean: %s' % str(np.mean(transition_matrix))
print 'N Updates Max: ' + str(np.abs(np.array(transition_matrix)).max())

N = np.abs(np.array(transition_matrix)).max()
simulation = [example_state]
maxp = np.array(transition_matrix).max()
if N > maxp:
    state = np.zeros(example_state.shape)
    for x in range(state.shape[0]):
        for y in range(state.shape[1]):
            if transition_matrix[x,y] < 0:
                state[x,y] -= 1
            elif transition_matrix[x,y] > 0:
                state[x, y] += 1
    simulation.append(state)
    transition_matrix = state - example_state
imutils.bw_render(simulation, 100, False, '')