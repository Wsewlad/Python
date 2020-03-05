#!/usr/bin/python3

import datetime
from state import State
from heapq import heappush, heappop, heapify
from itertools import chain

class Puzzle:
    def __init__(self):
        self.n = 0
        self.data_len = 0
        self.opened = []
        #self.closed = []
        self.closed = set()
        self.initial_data = []
        self.goal_data = []
        self.not_validated_tiles = []
        self.validated_tiles = []

        heapify(self.opened)
        #heapify(self.closed)


    def validate_tiles(self, tiles_line):
        res = tiles_line.split()
        if len(res) != self.n:
            raise Exception('*', "Wrong number of tiles")
        for tile in res:
            if not tile.isdigit():
                raise Exception('*', f"Tile '{tile}' is not number or is negative")
            if tile in self.validated_tiles:
                raise Exception('*', f"Tile '{tile}' duplicated")
            if not tile in self.not_validated_tiles:
                raise Exception('*', f"Tile '{tile}' is not in range 0:{self.data_len}")
            self.validated_tiles.append(tile)
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

        self.not_validated_tiles = [str(i) for i in range(self.data_len)]
        for value in content_list:
            if value.strip().startswith("#"):
                continue
            validation_result = self.validate_tiles(value.split("#")[0])
            self.initial_data.append(validation_result)
            if len(self.initial_data) == self.n:
                break
        if len(self.not_validated_tiles) != len(self.validated_tiles):
            raise Exception('*', "Wrong number of tiles")


    def f(self, current):
        return self.h(current) + current.level


    def h(self, current):
        res = 0
        for i in range(0, self.n):
            for j in range(0, self.n):
                i2, j2 = current.find(self.goal_data, current.data[i][j])
                res += abs(i - i2) + abs(j - j2)
        return res

    def generate_goal_data(self):
        self.goal_data = [[0] * self.n for i in range(self.n)]
        d = "r"
        i = 0
        j = 0
        for k in range(1, self.data_len):
            if d == "r":  # right
                if j < self.n and self.goal_data[i][j] == 0:
                    self.goal_data[i][j] = k
                else:
                    i += 1; j -= 1; d = "d"
            if d == "d":  # down
                if i < self.n and self.goal_data[i][j] == 0:
                    self.goal_data[i][j] = k
                else:
                    i -= 1; j -= 1; d = "l"
            if d == "l":  # left
                if j >= 0 and self.goal_data[i][j] == 0:
                    self.goal_data[i][j] = k
                else:
                    i -= 1; j += 1; d = "u"
            if d == "u":  # up
                if i >= 0 and self.goal_data[i][j] == 0:
                    self.goal_data[i][j] = k
                else:
                    i += 1; j += 1; d = "r"
            if d == "r":  # right
                if j < self.n and self.goal_data[i][j] == 0:
                    self.goal_data[i][j] = k
            if d == "r":
                j += 1
            elif d == "d":
                i += 1
            elif d == "l":
                j -= 1
            elif d == "u":
                i -= 1


    def inversions_count(self, line_input, line_goal):
        inv = 0
        for i in range(self.data_len - 1):
            for j in range(i + 1, self.data_len):
                if line_goal.index(line_input[i]) > line_goal.index(line_input[j]):
                    inv += 1
        return inv

    def is_solvable(self):
        line_input = list(chain.from_iterable(self.initial_data))
        line_goal = list(chain.from_iterable(self.goal_data))
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


    def solve(self):
        initial_state = State(self.initial_data)
        initial_state.fval = self.f(initial_state)
        heappush(self.opened, initial_state)
        goal_state = None
        while len(self.opened) > 0:
            current_state = heappop(self.opened)
            self.closed.add(current_state)
            print(len(self.opened))
            # if current_state.data == self.goal_data:
            #     goal_state = current_state
            #     break
            for state in current_state.expand():
                if state.data == self.goal_data:
                    goal_state = current_state
                    return
                found_states = self.opened + self.closed
                if state.data not in [st.data for st in found_states]:
                    state.fval = self.f(state)
                    heappush(self.opened, state)

        path_to_goal = []
        temp_state = goal_state
        while temp_state:
            path_to_goal.append(temp_state)
            temp_state = temp_state.last_node
            if not temp_state:
                break

        path_to_goal.reverse()
        for i in path_to_goal:
            i.print()
