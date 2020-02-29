#!/usr/bin/python3

import sys
from state import State
from heapq import heappush, heappop, heapify
import re

class Puzzle:
    def __init__(self):
        self.n = 0
        self.opened = []
        self.closed = []
        self.initialData = []
        self.goalData = []
        self.notValidatedTiles = set()
        self.validatedTiles = set()
        self.solved = False

        heapify(self.opened)
        heapify(self.closed)


    def validate_tiles(self, tilesLine):
        res = tilesLine.split(" ")
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


    def parse_content(self, content):
        contentList = list(filter(None, map(str.strip, content.strip().split("\n"))))
        firstTilesLineIdx = 0
        for idx in range(0, len(contentList)):
            value = contentList[idx].split("#")[0].strip()
            if value.isdigit():
                self.n = int(value)
                print(value)
                firstTilesLineIdx = idx + 1
                break
        if self.n == 0:
            print("No valid Puzzle size found")
            return 0
        if len(contentList) - firstTilesLineIdx < self.n:
            print("Wrong number of tiles")
            return 0
        self.notValidatedTiles = {str(i) for i in range(0, self.n * self.n)}
        for idx in range(firstTilesLineIdx, len(contentList)):
            if contentList[idx].strip().startswith("#"):
                continue
            validation_result = self.validate_tiles(re.sub('\s+', ' ', contentList[idx]).split("#")[0])
            if validation_result["status"] == False:
                print(validation_result["reason"])
                return 0
            self.initialData.append(validation_result["result"])
            if len(self.initialData) == self.n:
                break
        if len(self.notValidatedTiles) > 0:
            print("Wrong number of tiles")
            return 0


    def f(self, current):
        """ Heuristic Function to calculate hueristic value f(x) = h(x) + g(x) """
        return self.h(current.data) + current.level


    def h(self, current):
        """ Calculates the different between the given puzzles """
        temp = 0
        for i in range(0, self.n):
            for j in range(0, self.n):
                if current.data[i][j] != self.goalData[i][j] and current.data[i][j] != '0':
                    temp += 1
        return temp


    def generate_goal_data(self):
        nbr = self.n * self.n
        self.goalData = [[0] * self.n for i in range(self.n)]
        d = "r"
        i = 0
        j = 0
        for k in range(1, nbr):
            if d == "r": # right
                if j < self.n and self.goalData[i][j] == 0: self.goalData[i][j] = k
                else: i += 1; j -= 1; d = "d"
            if d == "d": # down
                if i < self.n and self.goalData[i][j] == 0: self.goalData[i][j] = k
                else: i -= 1; j -= 1; d = "l"
            if d == "l": # left
                if j >= 0 and self.goalData[i][j] == 0: self.goalData[i][j] = k
                else: i -= 1; j += 1; d = "u"
            if d == "u": # up
                if i >= 0 and self.goalData[i][j] == 0: self.goalData[i][j] = k
                else: i += 1; j += 1; d = "r"
            if d == "r": # right
                if j < self.n and self.goalData[i][j] == 0: self.goalData[i][j] = k
            if   d == "r": j += 1
            elif d == "d": i += 1
            elif d == "l": j -= 1
            elif d == "u": i -= 1


    def solve(self):
        self.generate_goal_data()
        initialState = State(self.initialData, 0, 0)
        initialState.fval = self.f(self.initialData)
        heappush(self.opened, initialState)

        while self.opened.count() != 0 and self.solved != True:
            currentState = heappop(self.opened)
            if self.h(cur.data, goal) == 0:
                self.solved = True
            else:
                heappush(self.closed, currentState)

                for i in cur.generate_child():
                    i.fval = self.f(i,goal)
                    self.open.append(i)
                self.closed.append(cur)
                del self.open[0]
                self.open.sort(key = lambda x:x.fval, reverse=False)