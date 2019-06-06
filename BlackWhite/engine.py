import matplotlib.pyplot as plt
import scipy.ndimage as ndi
import numpy as np
import scipy.misc
import imutils
import os


k0 = [[1,1,1],[1,1,1],[1,1,1]]

k1 = [[1,1,1],[1,0,1],[1,1,1]]

k2 = [[1,1,1,1],
      [1,0,0,1],
      [1,0,0,1],
      [1,1,1,1]]

k3 = [[0,0,0,0],
      [0,1,1,0],
      [0,1,1,0],
      [0,0,0,0]]


def save_states(states):
    ii = 0
    for state in states:
        scipy.misc.imsave('demo/state' + str(ii) + '.png', state)
        ii += 1


def diffuse(ngen, state):
    gen = 0
    generations = [state]
    dfu = [[1,1,1,1,1],  # [1]: 16 occurrences (16)
           [1,2,2,2,1],  # [2]: 8 occurrences (16)
           [1,2,1,2,1],  # [3]: 1 occurrance (3)
           [1,2,2,2,1],  # SUM 35 = Maxed out
           [1,1,1,1,1]]

    flipped = np.zeros(state.shape).flatten()
    while gen < ngen:
        world = ndi.convolve(np.array(state), np.array(dfu))/10
        avg = world.mean()
        minima = world.min()
        dims = state.shape
        ii = 0
        state = state.flatten()
        for cell in world.flatten():
            if state[ii] == 0:
                if minima <= cell < avg and minima % 8 == 0:
                    flipped[ii] += 1    # Adding time-evolving decay
                    state[ii] = 255
            elif cell >= avg and cell % 5 == 0:
                flipped[ii] += 1      # Adding time-evolving decay
                state[ii] = 255
            elif state[ii] > 50:
                state[ii] = 1
            if flipped[ii] >= int(len(generations) - len(generations)/4):
                state[ii] = 1
            ii += 1
        state = state.reshape(dims[0],dims[1])
        generations.append(state)
        gen += 1
    return generations


def generate_noise(data):
    dims = np.array(data).shape
    return np.random.random_integers(1,255,dims[0]*dims[1]).reshape(dims)


width = 250
height = 250
circle = imutils.draw_centered_circle(np.zeros((width, height)), int(width/3), False)
noise = np.array(np.random.random_integers(0, 255, width*height)).reshape((width,height))
# imutils.filter_preview({'k1': ndi.convolve(circle, np.array(k1), origin=0)/100,
#                         'k3': ndi.convolve(circle+noise, k3, origin=0)/100})
test_image = plt.imread('amzn.jpeg')[:, :, 0] + generate_noise(plt.imread('amzn.jpeg')[:, :, 0])
# test_image = circle + noise
sim = diffuse(250, test_image)
imutils.bw_render(sim, 50, False, '')

opt = str(raw_input('Dou  you want to save this simulation? (y/n): '))

