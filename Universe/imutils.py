from matplotlib.animation import FFMpegWriter
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import scipy.ndimage as ndi
import numpy as np
import resource
import os


def swap(fname, destroy):
    data = []
    for line in open(fname, 'r').readlines():
        data.append(line.replace('\n', ''))
    if destroy:
        os.remove(fname)
    return data


def bw_render(frames, frame_rate, save, file_name):
    f = plt.figure()
    film = []
    for frame in frames:
        film.append([plt.imshow(frame, 'gray_r')])
    a = animation.ArtistAnimation(f, film, interval=frame_rate, blit=True, repeat_delay=900)
    if save:
        writer = FFMpegWriter(fps=frame_rate, metadata=dict(artist='Me'), bitrate=1800)
        a.save(file_name, writer=writer)
    plt.show()


def color_render(frames, frame_rate, save, file_name):
    f = plt.figure()
    film = []
    for frame in frames:
        film.append([plt.imshow(frame, 'rainbow')])
    a = animation.ArtistAnimation(f, film, interval=frame_rate, blit=True, repeat_delay=900)
    if save:
        writer = FFMpegWriter(fps=frame_rate, metadata=dict(artist='Me'), bitrate=1800)
        a.save(file_name, writer=writer)
    plt.show()


def LIH_flat_map_creator(state):
    """
    LoopInvariantHoisting to preallocate a map, that
    pairs a flattened index of a corresponding state to
    an x-y position.
    :param state:
    :return:
    """
    index_map = {}
    ii = 0
    for x in range(state.shape[0]):
        for y in range(state.shape[1]):
            index_map[ii] = [x, y]
            ii += 1
    return index_map


def check_mem_usage():
    """
    Return the amount of RAM usage, in bytes, being consumed currently.
    :return (integer) memory:
    """
    mem = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return mem


def filter_preview(images):
    f, ax = plt.subplots(1, len(images.keys()))
    II = 0
    for image in images.keys():
        ax[II].imshow(images[image], 'gray_r')
        ax[II].set_title(image)
        II += 1
    plt.show()


def sub2ind(subs, dims):
    """
    Given a 2D Array's subscripts, return it's
    flattened index
    :param subs:
    :param dims:
    :return:
    """
    ii = 0
    indice = 0
    for y in range(dims[1]):
        for x in range(dims[0]):
            if subs[0] == x and subs[1] == y:
                indice = ii
            ii += 1
    return indice


def ind2sub(index,dims):
    """
    Given an index and array dimensions,
    convert an index to [x,y] subscript pair.
    :param index:
    :param dims:
    :return tuple - subscripts :
    """
    subs = []
    ii = 0
    for x in range(dims[0]):
        for y in range(dims[1]):
            if index==ii:
                subs = [x, y]
                return subs
            ii +=1
    return subs


def spawn_random_point(state):
    # Initialize a random position
    x = np.random.random_integers(0, state.shape[0], 1)[0]
    y = np.random.random_integers(0, state.shape[1], 1)[0]
    return [x, y]


def spawn_random_walk(position, n_steps):
    choice_pool = np.random.randint(1, 10, n_steps)
    random_walk = list()
    for step in choice_pool:
        directions = {1: [position[0]-1, position[1]-1],
                      2: [position[0], position[1]-1],
                      3: [position[0]+1, position[1]-1],
                      4: [position[0]-1, position[1]],
                      5: position,
                      6: [position[0]+1, position[1]],
                      7: [position[0]-1, position[1]+1],
                      8: [position[0], position[1]+1],
                      9: [position[0]+1, position[1]+1]}
        position = directions[step]
        random_walk.append(directions[step])
    return random_walk


def draw_centered_circle(canvas, radius,value, show):
    cx = canvas.shape[0]/2
    cy = canvas.shape[1]/2
    for x in np.arange(cx - radius, cx + radius, 1):
        for y in np.arange(cy - radius, cy + radius, 1):
            r = np.sqrt((x-cx)**2 + ((cy-y)**2))
            if r <= radius:
                try:
                    canvas[x, y] = value
                except IndexError:
                    pass
    if show:
        plt.imshow(canvas, 'gray_r')
        plt.show()
    return canvas


def find_local_images():
    os.system('locate *.jpg* >> command.txt')
    jpegs = swap('command.txt', True)
    os.system('locate *.png* >> command.txt')
    pngs = swap('command.txt', True)
    return jpegs, pngs


def sharpen(image, level):
    imat = np.array(image)
    kernel = [[0,0,0],[0,level,0],[0,0,0]]
    return ndi.convolve(imat,kernel)


def draw_centered_box(state, sz, value, show):
    cx = state.shape[0]/2
    cy = state.shape[1]/2
    state[cx-sz:cx+sz,cy-sz:cy+sz] = value
    if show:
        plt.imshow(state)
        plt.show()
    return state


def kernel_gen(bit_depth, seed_size, kernel_sz):
    kernels = []
    for i in range(seed_size):
        kernels.append(
            np.random.random_integers(0, bit_depth,
                                      kernel_sz*kernel_sz).reshape((kernel_sz, kernel_sz)))
    return kernels


def draw_blue_point_cloud(width, height, state, n_particles, radius, show):
    points = []
    cx = width / 2
    cy = height / 2
    # Add blue particle cloud
    for bpt in range(n_particles):
        [x, y] = spawn_random_point(state[:, :, 2])
        r = np.sqrt(((cx - x) ** 2 + (cy - y) ** 2))
        if r <= radius and len(np.nonzero(state[x,y,:])) == 1:
            state[x, y, 2] = 1
            points.append([x, y])
    if show:
        plt.title('%d Particle Cloud' % len(points))
        plt.imshow(state)
        plt.show()
    return state, points
