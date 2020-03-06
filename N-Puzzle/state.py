#!/usr/bin/python3

from copy import deepcopy
from itertools import chain

class State:
    def __init__(self, data, level=0, fval=0, last_node=None):
        self.data = data
        self.n = len(data)
        self.level = level
        self.fval = fval
        self.last_node = last_node
        self.oneline_data = tuple(list(chain.from_iterable(self.data)))

    def __lt__(self, other):
        return self.fval < other.fval

    def expand(self):
        x, y = self.find(self.data, 0)
        val_list = [[x, y - 1], [x, y + 1], [x - 1, y], [x + 1, y]]
        children = []
        for i in val_list:
            child = self.move(self.data, x, y, i[0], i[1])
            if child:
                child_node = State(child, self.level + 1, 0, self)
                children.append(child_node)
        return children

    def move(self, data, x1, y1, x2, y2):
        if x2 >= 0 and x2 < self.n and y2 >= 0 and y2 < self.n:
            new_data = deepcopy(data)
            new_data[x2][y2], new_data[x1][y1] = new_data[x1][y1], new_data[x2][y2]
            return new_data

    def find(self, data, x):
        for i, line in enumerate(data):
            if x in line:
                return i, line.index(x)

    def print(self):
        for i in range(0, len(self.data)):
            print(self.data[i])
        print("\n")