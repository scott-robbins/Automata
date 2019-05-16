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


def checker(ratio, dims, preview, isColor):
    canvas = np.zeros((dims[0], dims[1])).flatten()
    for II in range((dims[0]*dims[1])-1):
        if II % ratio == 0:
            canvas[II] = 1
    if preview:
        if isColor:
            plt.imshow(canvas.reshape(dims[0], dims[1]))
        else:
            plt.imshow(canvas.reshape(dims[0], dims[1]), 'gray_r')
        plt.show('SEED [dots | stripes]')
        plt.show()
    return canvas.reshape(dims)


def center_box(size,dims,preview,isColor):
    canvas = np.zeros((dims[0], dims[1]))

    rx = dims[0] - int(dims[0]/size)
    ry = dims[1] -dims[1]/size
    lx = int(dims[0]/size)
    ly = int(dims[1]/size)
    canvas[lx:rx,ly:ry] = 1
    if preview:
        if isColor:
            plt.imshow(canvas)
        else:
            plt.imshow(canvas.reshape(dims),'gray_r')
        plt.title('SEED [BOX]')
        plt.show()
    return canvas


def simulate(state, ngen, kernel):
    gen = 0
    generations = []
    while gen < ngen:
        generations.append(state)
        space = ndi.convolve(state, kernel)
        dims = state.shape
        nextstate = state.flatten()
        II = 0
        for cell in space.flatten():
            if cell % 2 == 0:
                nextstate[II] = 1
            else:
                nextstate[II] = 0
            II += 1
            state = nextstate.reshape(dims)
        gen += 1

    return generations


kernel0 = [[1,1,1],
           [1,0,1],
           [1,1,1]]

kernel1 = [[1,1,1,1,1],
           [1,1,1,1,1],
           [1,1,0,1,1],
           [1,1,1,1,1],
           [1,1,1,1,1]]

space = checker(3,[250, 250], True, False)
box = center_box(3, [250, 250], True, False)
space2 = checker(9,[250, 250], True, False)
t0 = time.time()

sim = simulate(box,100,kernel0)

t1 = time.time()
print "Simulation finished. Beginning Rendering. ["+str(t1-t0)+"s]"
render(sim,False,70)

render(simulate(box,100,kernel1), False, 70)
render(simulate(space,200,kernel0),False,70)
render(simulate(space2,200,kernel0),False,70)
render(simulate(space,200,kernel1), False, 70)
render(simulate(box,100,kernel1), False, 70)