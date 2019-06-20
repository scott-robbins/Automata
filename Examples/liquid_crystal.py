import matplotlib.pyplot as plt, matplotlib.animation as animation
import time, numpy as np, scipy.ndimage as ndi


def render(matrices, isColor, speed):
    reel = []
    f = plt.figure()
    for frames in matrices:
        if isColor:
            reel.append([plt.imshow(frames)])
        else:
            reel.append([plt.imshow(frames, 'gray_r')])
    a = animation.ArtistAnimation(f, reel, interval=speed, blit=True, repeat_delay=500)
    plt.show()


def special_render(seed,matrices,isColor,speed):
    # f, (ax0, ax1) = plt.subplots(1, 2)
    # ax0.imshow(m2.pop())
    # ax1.imshow(seed)
    # plt.show()
    reel = []
    f, (ax0, ax1) = plt.subplots(1,2)
    for frame in matrices:
        if isColor:
            reel.append([ax0.imshow(seed)])
            reel.append([ax1.imshow(frame)])
        else:
            reel.append([ax0.imshow(seed,'gray_r')])
            reel.append([ax1.imshow(frame,'gray_r')])
    a = animation.ArtistAnimation(f, reel,interval=speed,blit=True,repeat_delay=500)
    plt.show()


def simulate(ngenerations, kernel, state, Dense, dims):
    gen = 0
    frames = []
    while gen < ngenerations:
        frames.append(state)
        world = ndi.convolve(state, kernel).flatten()
        nextstate, cells = swarm(world, state.flatten(), Dense)
        state = nextstate.reshape(dims)
        gen += 1
    return frames


def swarm(world, state, density):
    nclusters = 0
    ii = 0
    for cell in world:
        if cell >= density:
            state[ii] -= 1
        else:
            state[ii] += 1
        if state[ii] % density == 0:
            state[ii] = 0
        ii += 1
    return state, nclusters


def main():
    width = 100
    height = 100

    k0 = [[2,1,2],
          [1,2,1],
          [2,1,2]]

    k1 = [[2,2,2,2,2],
          [2,1,1,1,2],
          [2,1,0,1,2],
          [2,1,1,1,2],
          [2,2,2,2,2]]

    k2 = [[1,1,0,1,1],
          [1,0,1,0,1],
          [0,1,0,1,0],
          [1,0,1,0,1],
          [1,1,0,1,1]]

    seed = np.random.randint(0, 2, width * height).reshape((width, height))

    matrices = simulate(100, k2, seed, 12, seed.shape)
    special_render(seed,matrices, False, 40)

    m2 = simulate(100,k0,seed,6,seed.shape)
    special_render(seed, m2, False, 40)


if __name__ == '__main__':
    main()
