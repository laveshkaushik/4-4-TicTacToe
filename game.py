import random
import time
import sys

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
            cells.append(NAMES[state[i][j]].center(7));
    print BOARD_FORMAT.format(*cells)


def emptystate():
    return [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]


def gameover(state):
    for i in range(4):
        if state[i][0] != EMPTY and state[i][0] == state[i][1] and state[i][0] == state[i][2] and state[i][0] == state[i][3]:
            return state[i][0]
        if state[0][i] != EMPTY and state[0][i] == state[1][i] and state[0][i] == state[2][i] and state[0][i] == state[3][i]:
            return state[0][i]
    if state[0][0] != EMPTY and state[0][0] == state[1][1] and state[0][0] == state[2][2] and state[0][0] == state[3][3]:
        return state[0][0]
    if state[0][3] != EMPTY and state[0][3] == state[1][2] and state[0][3] == state[2][1] and state[0][3] == state[3][0]:
        return state[0][3]

    for i in range(4):
        for j in range(4):
            if state[i][j] == EMPTY:
                return EMPTY
    return DRAW


class Agent(object):
    def __init__(self, player, lossval=0, learning=True):
        self.values = {}
        self.epsilon = 0.1
        self.player = player
        self.lossval = lossval
        self.prevstate = None
        self.prevvalue = 0
        self.learning = learning
        self.alpha = 0.99

    def random(self, state):
        available = []
        for i in range(4):
            for j in range(4):
                if state[i][j] == EMPTY:
                    available.append((i,j))
        return random.choice(available)

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

    def add(self, state):
        winner = gameover(state)
        self.values[self.statetuple(state)] = self.winnerval(winner)

    def lookup(self, state):
        key = self.statetuple(state)
        if not key in self.values:
            self.add(state)
        return self.values[key]

    def greedy(self, state):
        maxval = -500000
        maxpos = None
        # printboard(state)
        for i in range(4):
            for j in range(4):
                if state[i][j] == EMPTY:
                    state[i][j] = self.player
                    val = self.lookup(state)
                    # print val,maxval
                    state[i][j] = EMPTY
                    if val > maxval:
                        maxval = val
                        maxpos = (i, j)
        # print maxpos
        return maxpos
