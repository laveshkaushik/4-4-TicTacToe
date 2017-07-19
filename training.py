import random
import sys
import time
import pickle

EMPTY = 0
PLAYER_X = 1
PLAYER_O = 2
DRAW = 3

BOARD_FORMAT = "-----------------------------------------\n| {0} | {1} | {2} | {3} |\n|---------------------------------------|\n| {4} | {5} | {6} | {7} |" \
               "\n|---------------------------------------|\n| {8} | {9} | {10} | {11} |\n|---------------------------------------|\n| {12} | {13} | {14} | {15} |\n-----------------------------------------"
NAMES = [' ', 'X', 'O']

def printboard(state):
    cells = []
    for i in range(4):
        for j in range(4):
            cells.append(NAMES[state[i][j]].center(7))
    print BOARD_FORMAT.format(*cells)


def emptystate():
    return [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]


def gameover(state, emptyset):
    for i in range(4):
        if state[i][0] != EMPTY and state[i][0] == state[i][1] and state[i][0] == state[i][2] and state[i][0] == state[i][3]:
            return state[i][0]
        if state[0][i] != EMPTY and state[0][i] == state[1][i] and state[0][i] == state[2][i] and state[0][i] == state[3][i]:
            return state[0][i]
    if state[0][0] != EMPTY and state[0][0] == state[1][1] and state[0][0] == state[2][2] and state[0][0] == state[3][3]:
        return state[0][0]
    if state[0][3] != EMPTY and state[0][3] == state[1][2] and state[0][3] == state[2][1] and state[0][3] == state[3][0]:
        return state[0][3]

    if len(emptyset):
        return EMPTY

    return DRAW


class Agent(object):
    def __init__(self, player, verbose=False, lossval=0, learning=True):
        self.values = {}
        self.epsilon = 0.1
        self.player = player
        self.lossval = lossval
        self.prevstate = None
        self.prevvalue = 0
        self.verbose = verbose
        self.learning = learning
        self.alpha = 0.99

    def statetuple(self, state):
        return tuple(state[0]),tuple(state[1]),tuple(state[2]),tuple(state[3])

    def winnerval(self, winner):
        if winner == self.player:
            return 1
        elif winner == DRAW:
            return 0
        elif winner == EMPTY:
            return 0.5
        else:
            return self.lossval

    def add(self, state, emptyset):
        winner = gameover(state, emptyset)
        self.values[self.statetuple(state)] = self.winnerval(winner)

    def lookup(self, state, emptyset):
        key = self.statetuple(state)
        if not key in self.values:
            self.add(state, emptyset)
        return self.values[key]

    def backup(self, nextval):
        if self.prevstate != None and self.learning:
            self.values[self.prevstate] += self.alpha * (nextval - self.prevvalue)

    def greedy(self, state, emptyset):
        maxval = -500000
        maxpos = None
        # printboard(state)
        if not self.verbose:
            for i,j in emptyset:
                state[i][j] = self.player
                val = self.lookup(state, emptyset)
                # print val,maxval
                state[i][j] = EMPTY
                if val > maxval:
                    maxval = val
                    maxpos = (i, j)
        else:
            cells = []
            for i in range(4):
                for j in range(4):
                    if state[i][j] == EMPTY:
                        state[i][j] = self.player
                        val = self.lookup(state, emptyset)
                        state[i][j] = EMPTY
                        if val > maxval:
                            maxval = val
                            maxpos = (i, j)
                        cells.append('{0:.3f}'.format(val).center(7))
                    else:
                        cells.append(NAMES[state[i][j]].center(7))
            print BOARD_FORMAT.format(*cells)
        self.backup(maxval)
        # print maxpos
        return maxpos

    def action(self, state, emptyset):
        r = random.random()
        # Exploratory move
        if r < self.epsilon:
            # print 'here'
            move = random.choice(list(emptyset))
        # Exploitation
        else:
            # print 'there'
            move = self.greedy(state, emptyset)
        state[move[0]][move[1]] = self.player
        self.prevstate = self.statetuple(state)
        self.prevvalue = self.lookup(state, emptyset)
        state[move[0]][move[1]] = EMPTY
        return move

    def episode_over(self, winner):
        self.backup(self.winnerval(winner))
        self.prevstate = None
        self.prevvalue = 0


class Human(object):
    def __init__(self, player):
        self.player = player

    def action(self, state, emptystate):
        printboard(state)
        action = raw_input('your move? ')
        move = (int(action.split(',')[0]),int(action.split(',')[1]))
        while not move in emptystate:
            action = raw_input('your move? ')
            move = (int(action.split(',')[0]), int(action.split(',')[1]))
        return move

    def episode_over(self,winner):
        if winner == DRAW:
            print 'GAME DRAW.'
        else:
            print 'Player {0} wins'.format(NAMES[winner])

def play(agent1, agent2):
    state = emptystate()
    emptyset = set()
    for i in range(4):
        for j in range(4):
            emptyset.add((i,j))

    for k in range(16):
        if k % 2 == 0:
            move = agent1.action(state, emptyset)
            state[move[0]][move[1]] = agent1.player
        else:
            move = agent2.action(state, emptyset)
            state[move[0]][move[1]] = agent2.player
        emptyset.remove(move)
        winner = gameover(state, emptyset)
        if winner != EMPTY:
            # print winner
            return winner

    # print winner
    return winner

if __name__ == '__main__':
    a1 = Agent(1, lossval=-1)
    a2 = Agent(2, lossval=-1)
    with open('/Users/lavesh/PycharmProjects/tictactoe/filename1.pickle', 'rb') as handle:
        c = pickle.load(handle)
    a2.values = c
    start = time.time()
    for i in range(5000000):
        if i%1000000==0:
            print i
        winner = play(a2, a1)
        a1.episode_over(winner)
        a2.episode_over(winner)
    end = time.time()
    print end-start
    with open('filename1.pickle', 'wb') as handle:
        pickle.dump(a2.values, handle, protocol=pickle.HIGHEST_PROTOCOL)
    '''
    a1.verbose = True
    while True:
        a2 = Human(1)
        winner = play(a1, a2)
        a1.episode_over(winner)
        a2.episode_over(winner)
    '''

'''
def tmp(x):
    a1 = Agent(1, lossval=-1)
    a2 = Agent(2, lossval=-1)
    for i in range(x):
        if i%100000 == 0:
            print i
        winner = play(a1, a2)
        a1.episode_over(winner)
        a2.episode_over(winner)

if __name__ == '__main__':
    pool = multiprocessing.Pool(processes=4)
    y = [300000,300000,300000,300000,300000,300000,300000,300000]
    r = pool.map(tmp,y)
    pool.close()
    print 'here'
    while True:
        a1 = Human(1)
        a2 = Agent(2, lossval=-1)
        winner = play(a1, a2)
        a1.episode_over(winner)
        a2.episode_over(winner)
'''