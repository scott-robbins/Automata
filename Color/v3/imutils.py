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
    for index in range(state.shape[0]*state.shape[1]):
        index_map[index] = ind2sub(index, [state.shape[0], state.shape[1]])
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


def draw_progress_bar(name, depth, index):
    os.system('clear')
    print '\033[1m'+'#'*6+' << \033[31m\033[3m '+name+' \033[0m\033[1m >> '+'#'*8+'\033[0m'
    bar = '#'
    for b in range(int(index/depth)*31):
        bar += '#'
    if index != depth:
        print '\033[1m' + bar + ' [\033[32m'+str(100*index/depth + 1)+'% Complete\033[0m\033[1m]\033[0m'
    else:
        print '\033[1m' + bar + ' [\033[32m100% Complete\033[0m\033[1m]\033[0m'
