#!/usr/bin/python3

import sys
from state import State
from heapq import heappush, heappop, heapify

class Puzzle:
    def __init__(self):
        self.n = 0
        self.data_len = 0
        self.opened = []
        self.closed = []
        self.initialData = []
        self.goalData = []
        self.notValidatedTiles = []
        self.validatedTiles = []
        self.solved = False

        heapify(self.opened)
        heapify(self.closed)


    def validate_tiles(self, tilesLine):
        res = tilesLine.split()
        if len(res) != self.n:
            raise Exception('*', "Wrong number of tiles")
        for tile in res:
            if not tile.isdigit():
                raise Exception('*', f"Tile '{tile}' is not number or is negative")
            if tile in self.validatedTiles:
                raise Exception('*', f"Tile '{tile}' duplicated")
            if not tile in self.notValidatedTiles:
                raise Exception('*', f"Tile '{tile}' is not in range 0:{self.data_len}")
            self.validatedTiles.append(tile)
        return list(map(int, res))


    def parse_content(self, content):
        content_list = list(filter(None, map(str.strip, content.strip().split("\n"))))
        for idx, value in enumerate(content_list):
            v = value.split("#")[0].strip()
            if v.isdigit():
                self.n = int(v)
                self.data_len = self.n ** 2
                content_list = content_list[idx + 1:]
                break
        else:
            raise Exception('*', "No valid Puzzle size found")

        if len(content_list) < self.n:
            raise Exception('*', "Wrong number of tiles")

        self.notValidatedTiles = [str(i) for i in range(self.data_len)]
        for value in content_list:
            if value.strip().startswith("#"):
                continue
            validation_result = self.validate_tiles(value.split("#")[0])
            self.initialData.append(validation_result)
            if len(self.initialData) == self.n:
                break
        if len(self.notValidatedTiles) != len(self.validatedTiles):
            raise Exception('*', "Wrong number of tiles")


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
        self.goalData = [[0] * self.n for i in range(self.n)]
        d = "r"
        i = 0
        j = 0
        for k in range(1, self.data_len):
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
        for i in range(self.data_len - 1):
            for j in range(i + 1, self.data_len):
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
        if self.n % 2:
            return not inv_count % 1
        else:
            pos = line_goal.index(0) // self.n
            if pos & 1:
                return not inv_count % 1
            else:
                return inv_count % 1

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
            print(len(self.closed))
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
