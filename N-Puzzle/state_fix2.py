#!/usr/bin/python3
from copy import deepcopy

class State:
    def __init__(self, data, level=0, fval=0, last_node=None):
        self.data = data
        self.level = level
        self.fval = fval
        self.last_node = last_node

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

    def move(self, puz, x1, y1, x2, y2):
        if x2 >= 0 and x2 < len(self.data) and y2 >= 0 and y2 < len(self.data):
            temp_puz = deepcopy(puz)
            temp_puz[x2][y2], temp_puz[x1][y1] = temp_puz[x1][y1], temp_puz[x2][y2]
            return temp_puz
            
    def find(self, puz, x):
        for i, line in enumerate(puz):
            if x in line:
                return i, line.index(x)


    def print(self):
        for i in range(len(self.data)):
            print(self.data[i])
        print("\n")