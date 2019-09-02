import matplotlib.pyplot as plt
import numpy as np
import imutils


class Organism:
    x = 0
    y = 0
    flavor = ''
    mode = 0
    size = 0
    STYLES = {'circle', 'square'}
    EIGEN = [0, 1, 2, 3]
    state = [[]]
    DEBUG = False

    def __init__(self, type, energy_level, radius):
        if self.build(type, energy_level):
            if self.DEBUG:
                print 'Building %s' % type
            ''' Initialize the Organism '''
            self.flavor = type
            self.mode = energy_level
            self.size = radius
            self.state = self.reveal(self.DEBUG)
            self.physics = Model(self)

    def build(self, t, e):
        if t in self.STYLES and e in self.EIGEN:
            return True
        else:
            return False

    def modify_state(self, new_state):
        if new_state in self.EIGEN:
            self.mode = new_state
            self.state = self.reveal(self.DEBUG)

    def reveal(self, show):
        if self.flavor == 'circle':
            sz = int(np.pi*self.size)
            state = np.zeros((sz,sz))

            if self.mode == 0:
                return imutils.draw_centered_circle(state, self.size, 1, show)

            if self.mode == 1:
                chunks = np.linspace(0, 2 * self.size, 4)
                r = self.size / 3
                t = state[int(chunks[1]):int(chunks[2]), int(chunks[1]):int(chunks[2])]
                pad = np.zeros(t.shape)
                circ = imutils.draw_centered_circle(np.zeros(t.shape), r, 1, False)
                blank = np.concatenate((pad,pad,pad,pad),1)
                mid = np.concatenate((pad,circ,circ,pad),1)
                state = np.concatenate((blank,mid,mid,blank),0)
                if show:
                    plt.imshow(state, 'gray')
                    plt.show()

            if self.mode == 2:
                chunks = np.linspace(0, 2*self.size, 4)
                r = self.size/3
                t = state[int(chunks[1]):int(chunks[2]), int(chunks[1]):int(chunks[2])]
                pad = np.zeros(t.shape)
                circ = imutils.draw_centered_circle(np.zeros(t.shape), r, 1, False)

                top = np.concatenate((t,circ,t),1)
                low = np.concatenate((t,circ,t),1)
                nul = np.concatenate((pad,pad,pad),1)
                state = np.concatenate((nul,top,low,nul),0)
                if show:
                    plt.imshow(state, 'gray')
                    plt.show()

            if self.mode == 3:
                cxs = np.linspace(0, 2*self.size, 4)
                cys = np.linspace(0, 2*self.size, 3)
                slice = state[int(cxs[1]):int(cxs[2]),
                              int(cys[1]):int(cys[2])]

                empty = np.zeros(slice.shape)
                circ = imutils.draw_centered_circle(slice,self.size/3,1,False)
                blank = np.concatenate((empty,empty), 1)
                mid = np.concatenate((circ,circ),1)
                mode = np.concatenate((blank,mid,blank), 0)
                state = mode
                # TODO: Add trim
                if show:
                    plt.imshow(state, 'gray')
                    plt.show()

        if self.flavor == 'square':
            sz = int(3*self.size)
            state = np.zeros((sz, sz))
            if self.mode == 0:
                return imutils.draw_centered_box(state, self.size, 1, show)

            if self.mode == 1:
                cxs = np.array(np.linspace(0, 3*self.size, 6))
                state[int(cxs[1]):int(cxs[2]),
                      int(cxs[1]):int(cxs[2])] = 1
                state[int(cxs[3]):int(cxs[4]),
                      int(cxs[1]):int(cxs[2])] = 1
                state[int(cxs[3]):int(cxs[4]),
                      int(cxs[3]):int(cxs[4])] = 1
                state[int(cxs[1]):int(cxs[2]),
                      int(cxs[3]):int(cxs[4])] = 1

            if self.mode == 2:
                cxs = np.array(np.linspace(0, 3 * self.size, 6))
                state[int(cxs[1]):int(cxs[2]),
                      int(cxs[1]):int(cxs[4])] = 1
                state[int(cxs[3]):int(cxs[4]),
                      int(cxs[1]):int(cxs[4])] = 1

            if self.mode == 3:
                cxs = np.array(np.linspace(0, 3 * self.size, 6))
                state[int(cxs[1]):int(cxs[4]),
                      int(cxs[1]):int(cxs[2])] = 1
                state[int(cxs[1]):int(cxs[4]),
                      int(cxs[3]):int(cxs[4])] = 1
            if show:
                plt.imshow(state, 'gray')
                plt.show()

        return state

    def set_position(self, x1, y1):
        self.x = x1
        self.y = y1


class Model:
    types = ['circle', 'square']
    transition_allocations = {}

    def __init__(self, object):
        if self.validate_organism(object):
            possible_states = object.EIGEN
            std_model = []
            for value in possible_states:
                probability = 1/float(len(possible_states))  # Normalized/Even Probabilities
                std_model.append(probability)
                self.transition_allocations[value] = probability
        else:
            print '\033[1m\033[31m** Unknown Organism! **\033[0m'

    def validate_organism(self, organism):
        if organism.flavor in self.types:
            return True
        else:
            return False
# Testing Organism Creation
# print Organism('circle', 1, 10).state.shape
# print Organism('circle', 2, 10).state.shape
# print Organism('circle', 3, 10).state.shape
# print Organism('square', 1, 10).state.shape
# print Organism('square', 2, 10).state.shape

# Testing Organism modification/evolution
# test = Organism('square', 0, 10)
# plt.imshow(test.state, 'gray')
# plt.show()
#
# test.modify_state(1)
# plt.imshow(test.state, 'gray')
# plt.show()

