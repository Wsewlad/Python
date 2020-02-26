#!/usr/bin/python3

from state import State
from heapq import heappush, heappop, heapify
import re

class Puzzle:
    def __init__(self):
        self.n = 0
        self.opened = []
        self.closed = []
        self.inputData = []
        self.goal = []
        self.notValidatedTiles = set()
        self.validatedTiles = set()

    def validate_tiles(self, tilesList):
        res = list(filter(None, map(str.strip, tilesList)))
        if len(res) != self.n:
            return {"status": False, "result": res, "reason": "Wrong number of tiles"}
        for tile in res:
            if tile.isdigit() == False:
                return {"status": False, "result": res, "reason": "Tile '{}' is not number or is negative".format(tile)}
            if tile in self.validatedTiles:
                return {"status": False, "result": res, "reason": "Tile '{}' duplicated".format(tile)}
            if tile in self.notValidatedTiles:
                self.validatedTiles.add(tile)
                self.notValidatedTiles.remove(tile)
            else:
                return {"status": False, "result": res, "reason": "Tile '{}' is not in range 0:{}".format(tile, self.n * self.n)}
        return {"status": True, "result": res}


    def parse_input_file(self, fname):
        puzzle = []
        with open(fname, "r") as file:
            for line in file:
                value = line.split("#")[0].strip()
                if value.isdigit():
                    self.n = int(value)
                    print(value)
                    break

            if self.n == 0:
                print("No valid Puzzle size found")
                return 0

            self.notValidatedTiles = {str(i) for i in range(0, self.n * self.n)}

            puzzleDatalines = file.readlines()
            if len(puzzleDatalines) < self.n:
                print("No valid number of data rows")
                return 0

            for line in puzzleDatalines:
                if line.strip().startswith("#"):
                    continue
                validation_result = self.validate_tiles(re.sub('\s+', ' ', line).split("#")[0].split(" ", self.n - 1))
                if validation_result["status"] == False:
                    print(validation_result["reason"])
                    return 0
                print(validation_result["result"])
                

    def f(self, current):
        """ Heuristic Function to calculate hueristic value f(x) = h(x) + g(x) """
        return self.h(current.data) + current.level


    def h(self, start):
        """ Calculates the different between the given puzzles """
        temp = 0
        for i in range(0,self.n):
            for j in range(0,self.n):
                if start[i][j] != self.goal[i][j] and start[i][j] != '_':
                    temp += 1
        return temp


    def generate_goal_data():
        nbr = self.n * self.n
        self.goal = [[0] * self.n for i in range(self.n)]
        d = "r"
        i = 0
        j = 0
        for k in range(1, nbr):
            if d == "r": # right
                if j < n and self.goal[i][j] == 0: self.goal[i][j] = k
                else: i += 1; j -= 1; d = "d"
            if d == "d": # down
                if i < n and self.goal[i][j] == 0: self.goal[i][j] = k
                else: i -= 1; j -= 1; d = "l"
            if d == "l": # left
                if j >= 0 and self.goal[i][j] == 0: self.goal[i][j] = k
                else: i -= 1; j += 1; d = "u"
            if d == "u": # up
                if i >= 0 and self.goal[i][j] == 0: self.goal[i][j] = k
                else: i += 1; j += 1; d = "r"
            if d == "r": # right
                if j < n and self.goal[i][j] == 0: self.goal[i][j] = k
            if   d == "r": j += 1
            elif d == "d": i += 1
            elif d == "l": j -= 1
            elif d == "u": i -= 1


    def solve(self):
        """ Accept Start and Goal Puzzle state"""
        print("Enter the start state matrix \n")
        start = self.accept()

        start = State(start,0,0)
        start.fval = self.f(start,goal)
        """ Put the start node in the open list"""
        self.open.append(start)
        print("\n\n")
        while True:
            cur = self.open[0]
            print("")
            print("  | ")
            print("  | ")
            print(" \\\'/ \n")
            for i in cur.data:
                for j in i:
                    print(j,end=" ")
                print("")
            """ If the difference between current and goal node is 0 we have reached the goal node"""
            if(self.h(cur.data,goal) == 0):
                break
            for i in cur.generate_child():
                i.fval = self.f(i,goal)
                self.open.append(i)
            self.closed.append(cur)
            del self.open[0]
            self.open.sort(key = lambda x:x.fval, reverse=False)