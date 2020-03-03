#!/usr/bin/python3

class State:
    def __init__(self, data, level, fval, last_node):
        self.data = data
        self.level = level
        self.fval = fval
        self.last_node = last_node

    def __lt__(self, other):
        return self.fval < other.fval

    def __eq__(self, other):
        if self.data != other.data:
            return False
        return True

    def expand(self):
        x, y = self.find(self.data, 0)
        val_list = [[x, y - 1], [x, y + 1], [x - 1, y], [x + 1, y]]
        children = []
        for i in val_list:
            child = self.move(self.data, x, y, i[0], i[1])
            if child is not None:
                child_node = State(child, self.level + 1, 0, self)
                children.append(child_node)
        return children

    def move(self, puz, x1, y1, x2, y2):
        if x2 >= 0 and x2 < len(self.data) and y2 >= 0 and y2 < len(self.data):
            temp_puz = [[x for x in row] for row in puz]
            temp = temp_puz[x2][y2]
            temp_puz[x2][y2] = temp_puz[x1][y1]
            temp_puz[x1][y1] = temp
            return temp_puz
        else:
            return None

            
    def find(self, puz, x):
        for i in range(0, len(self.data)):
            for j in range(0, len(self.data)):
                if puz[i][j] == x:
                    return i, j

    def print(self):
        for i in range(0, len(self.data)):
            print(self.data[i])
        print("\n")