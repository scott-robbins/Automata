import numpy as np, matplotlib.pyplot as plt, matplotlib. animation as animation
import scipy.ndimage as ndi


def render(matrices, speedOfLife, isColor):
    f = plt.figure()
    reel = []
    for matrix in matrices:
        if isColor:
            frame = plt.imshow(matrix)
        else:
            frame = plt.imshow(matrix,'gray_r')
        reel.append([frame])
    a = animation.ArtistAnimation(f, reel, interval=speedOfLife,blit=True,repeat_delay=1000)
    plt.show()


def simulate(ngen,seed,conv):
    gen = 0
    generations = []
    neural = []
    while gen <= ngen:
        generations.append(seed)
        world = ndi.convolve(seed, conv).flatten()
        nextstate = seed.flatten()
        land = np.zeros(world.shape)
        II = 0
        for cell in world:
            if cell >= 38:
                nextstate[II] = 0
            elif cell >=22 and nextstate[II] == 0:
                nextstate[II] = 1
            if cell < cell <=30 and nextstate[II] ==0 :
                nextstate[II] = 1
            if cell %10 == 0 or (cell >=44 or cell <=12):
                land[II] += 1
                nextstate[II] = 0
            if land[II] >= 60:
                nextstate[II] = 1
            II += 1
        # nextstate.reshape((seed.shape[0],seed.shape[1]))
        neural.append(world.reshape((seed.shape[0],seed.shape[1])))
        gen += 1
        seed =  nextstate.reshape((seed.shape[0],seed.shape[1]))
    return generations, neural


def main():
    filtahs = [[1,2,2,2,1],
               [2,2,3,2,2],
               [2,3,0,3,2],
               [2,2,3,2,2],
               [1,2,2,2,1]]
    
    mega = [[2,1,1,1,1,1],
            [1,2,2,2,2,1],
            [1,3,2,2,3,1],
            [1,2,1,1,2,1],
            [1,3,2,2,3,1],
            [1,1,1,1,1,2]]

    gravitas = [[1, 1, 1, 1, 1, 1, 1],
                [1, 2, 2, 2, 2, 2, 1],
                [1, 2, 3, 3, 3, 2, 1],
                [1, 2, 3, 0, 3, 2, 1],
                [1, 2, 3, 3, 3, 2, 1],
                [1, 2, 2, 2, 2, 2, 1],
                [1, 1, 1, 1, 1, 1, 1]]

    simulation, cellular_clusters = simulate(100, np.random.randint(0,2,15000).reshape((150,100)), filtahs)
    render(simulation,220,False)
    render(cellular_clusters,500,True)
    
    sim, cells = simulate(150, np.random.randint(0,2,15000).reshape((150,100)), mega)
    render(sim,250,False)
    render(cells,250,True)

    sim, cells = simulate(100, np.random.randint(0, 2, 30000).reshape((150, 200)), gravitas)
    render(sim, 200, False)
    render(cells, 200, True)
    
if __name__ == '__main__':
    main()

