
import numpy as np, matplotlib.pyplot as plt, matplotlib.animation as animation
import scipy.ndimage as ndi, time, resource


def render(matrices, speedOfLife):
    f = plt.figure()
    reel = []
    for matrix in matrices:
        frame = plt.imshow(matrix,'gray_r')
        reel.append([frame])
    a = animation.ArtistAnimation(f, reel, interval=speedOfLife,blit=True,repeat_delay=1000)
    plt.show()


def initialize_life():
    width = int(input('Enter width: '))
    height = int(input('Enter height: '))
    initial_state = np.random.randn(width * height).reshape((width, height)) > 0.5
    plt.imshow(initial_state, 'gray_r')
    plt.title('Initial State [GOL]')
    plt.show()

    initial = np.array(initial_state,dtype=int)
    return initial


def run(nGenerations, speed, seed):
    neighbors = [[1, 1, 1],
                 [1, 0, 1],
                 [1, 1, 1]]

    generations = []
    gen = 0
    start = time.time()
    while gen <= nGenerations:
        cells = ndi.convolve(seed, neighbors)
        nextState = seed.flatten()
        II = 0
        for cell in cells.flatten():
            # Check if its alive
            if nextState[II] == 1:
                if 2 <= cell < 4:
                    nextState[II] = 1
                else:
                    nextState[II] = 0
            elif cell == 3:
                nextState[II] = 1
            II += 1
        generations.append(nextState.reshape((seed.shape[0], seed.shape[1])))
        gen += 1
        seed = nextState.reshape((seed.shape[0], seed.shape[1]))
    # Animate the Game of Life Simulation!
    render(generations, speed)
    print "Finished Simulating" + str(nGenerations)+\
          " [" + str(time.time() - start) + "s Elapsed]"


def check_mem_usage():
    mem = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return mem


def main():
    print str(float(100 * check_mem_usage())/100000) +" Kb of initial RAM Overhead"
    initial_state = initialize_life()
    run(int(input('Enter Number of Generations to Simulate: ')),
        int(input('Enter Speed of Life [0-100]:\n') * 100 / 100), initial_state)
    print str(float(100*check_mem_usage())/100000) + " Kb of RAM Used"


if __name__ == '__main__':
    main()
