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
        return {"status": True, "result": list(map(int, res))}


    def parse_content(self, content):
        contentList = list(filter(None, map(str.strip, content.strip().split("\n"))))
        firstTilesLineIdx = 0
        for idx in range(0, len(contentList)):
            value = contentList[idx].split("#")[0].strip()
            if value.isdigit():
                self.n = int(value)
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
        return self.h(current) + current.level


    def h(self, current):
        res = 0
        for i in range(0, self.n):
            for j in range(0, self.n):
                i2, j2 = current.find(self.goalData, current.data[i][j])
                res += abs(i - i2) + abs(j - j2)
        return res


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

    @staticmethod
    def generate_one_line(data):
        line_data = []
        for line in data:
            for x in line:
                line_data.append(int(x))
        return line_data

    def inversions_count(self, line_input, line_goal):
        inv = 0
        for i in range(self.n * self.n - 1):
            for j in range(i + 1, self.n * self.n):
                if line_goal.index(line_input[i]) > line_goal.index(line_input[j]):
                    inv += 1
        return inv

    def is_solvable(self):
        line_input = self.generate_one_line(self.initialData)
        line_goal = self.generate_one_line(self.goalData)
        inv_count = self.inversions_count(line_input, line_goal)
        check_zero_position = abs(line_input.index(0) // self.n - line_goal.index(0) // self.n) + abs(line_input.index(0) % self.n - line_goal.index(0) % self.n)
        if check_zero_position % 2 == 0 and inv_count % 2 == 0:
            return True
        if check_zero_position % 2 == 1 and inv_count % 2 == 1:
            return True
        return False

    def is_puzzle_in(self, puzzle, list):
        for p in list:
            if p == puzzle:
                return p
        return None



    def solve(self):
        initialState = State(self.initialData, 0, 0, None)
        goalState = State(self.goalData, 0, 0, None)
        initialState.fval = self.f(initialState)
        heappush(self.opened, initialState)

        print(len(self.opened))
        tmp = None
        len_opened = len(self.opened)
        while len_opened != 0 and not self.solved:
            currentState = heappop(self.opened)
            heappush(self.closed, currentState)
            if currentState == goalState:
                print(len(self.opened))
                tmp = currentState
                self.solved = True
            else:
                for state in currentState.expand():
                    state.fval = self.f(state)
                    in_opened = self.is_puzzle_in(state, self.opened)
                    in_closed = self.is_puzzle_in(state, self.closed)

                    if in_opened is None and in_closed is None:
                        heappush(self.opened, state)
                    else:
                        if self.h(state) + state.level > currentState.level + 1 + self.h(state):
                            if in_closed is not None:
                                self.closed.remove(in_closed)
                                heappush(self.opened, state)
            len_opened = len(self.opened)

        tt = []
        while self.is_puzzle_in(tmp, self.closed) is not None:
            tt.append(tmp)
            tmp = tmp.last_node
            if tmp is None:
                break
            tmp = self.is_puzzle_in(tmp, self.closed)
        tt.reverse()
        for i in tt:
            i.print()

        print(len(tt))
