#!/usr/bin/python3

from state import State
from heapq import heappush, heappop, heapify
from itertools import chain
import datetime
import math

class Puzzle:
    def __init__(self, content, h):
        self.n = 0
        self.data_len = 0
        self.opened = []
        self.closed = set()
        self.initial_data = []
        self.goal_data = []
        self.not_validated_tiles = []
        self.validated_tiles = []
        self.opened_hash = {}
        self.goal_state = None
        self.solving_time = None
        self.line_goal = []
        self.heuristic_dict = {
            "eu" : self.get_euclidian_distance,
            "mn" : self.get_manhattan_distance,
            "mp" : self.get_misplaced_tiles_distance}

        self.heuristic = self.heuristic_dict[h]

        heapify(self.opened)
        self.parse_content(content)

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
        self.generate_goal_data()
        self.print_start()

    def get_manhattan_distance(self, current):
        dist = 0
        for i in current.oneline_data:
            if i == 0:
                continue
            c = current.oneline_data.index(i)
            g = self.line_goal.index(i)
            x = abs(g % self.n - c % self.n)
            y = abs(g / self.n - c / self.n)
            dist += x + y
        return dist

    def get_euclidian_distance(self, current):
        dist = 0
        for i in current.oneline_data:
            if i == 0:
                continue
            c = current.oneline_data.index(i)
            g = self.line_goal.index(i)
            x = (g % self.n - c % self.n) ** 2
            y = (g / self.n - c / self.n) ** 2
            dist += math.sqrt(x + y)
        return dist

    def get_misplaced_tiles_distance(self, current):
        dist = 0
        for val in current.oneline_data:
            if val == 0:
                continue
            if val != 0 and current.oneline_data.index(val) != self.line_goal.index(val):
                dist += 1
        return dist

    def f(self, current):
        return self.h(current) + current.level

    def h(self, current):
        return self.heuristic(current)

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

    # def inversions_count(self, line_input):
    #     #     inv = 0
    #     #     for i in range(self.data_len - 1):
    #     #         for j in range(i + 1, self.data_len):
    #     #             if self.line_goal.index(line_input[i]) > self.line_goal.index(line_input[j]):
    #     #                 inv += 1
    #     #     return inv
    #     #
    #     #
    #     # def is_solvable(self):
    #     #     line_input = list(chain.from_iterable(self.initial_data))
    #     #     self.line_goal = list(chain.from_iterable(self.goal_data))
    #     #     inv_count = self.inversions_count(line_input)
    #     #
    #     #     check_zero_position = abs(line_input.index(0) // self.n - self.line_goal.index(0) // self.n) + abs(line_input.index(0) % self.n - self.line_goal.index(0) % self.n)
    #     #     if check_zero_position % 2 == 0 and inv_count % 2 == 0:
    #     #         return True
    #     #     if check_zero_position % 2 == 1 and inv_count % 2 == 1:
    #     #         return True
    #     #     if self.n % 2:
    #     #         return not inv_count % 1
    #     #     else:
    #     #         pos = self.line_goal.index(0) // self.n
    #     #         if pos & 1:
    #     #             return not inv_count % 1
    #     #         else:
    #     #             return inv_count % 1

    def inversions_count(self, line_input, element, idx):
        inv = 0
        element_row = self.line_goal.index(element) / self.n
        element_col = self.line_goal.index(element) % self.n
        for e in line_input[idx + 1:]:
            if e == 0:
                continue
            e_row = self.line_goal.index(e) / self.n
            e_col = self.line_goal.index(e) % self.n
            if e_row < element_row or (e_row == element_row and e_col < element_col):
                inv += 1
        return inv

    def is_solvable(self):
        self.line_goal = list(chain.from_iterable(self.goal_data))
        line_input = list(chain.from_iterable(self.initial_data))
        zero_pos = line_input.index(0) / self.n + 1
        inv = 0
        for idx, val in enumerate(line_input):
            if val == 0:
                continue
            inv += self.inversions_count(line_input, val, idx)
        if self.n % 2 == 0:
            if (self.n / 2) % 2 == 0 and (zero_pos % 2 == 1 and inv % 2 == 0) or (zero_pos % 2 == 0 and inv % 2 == 1):
                return True
            elif (self.n / 2) % 2 == 1 and zero_pos % 2 == inv % 2 and zero_pos % 2 != zero_pos - 1:
                return True
            else:
                return False
        else:
            return inv % 2 == 0

    def print_start(self):
        print(f"Input puzzle ({self.n}x{self.n}):")
        if self.heuristic == self.get_euclidian_distance:
            print("Heuristic is Euclidian distance")
        elif self.heuristic == self.get_manhattan_distance:
            print("Heuristic is Manhattan distance")
        elif self.heuristic == self.get_misplaced_tiles_distance:
            print("Heuristic is Misplaced tiles")

        for i in self.initial_data:
            print(i)

    def print_result(self):
        path_to_goal = []
        temp_state = self.goal_state
        while temp_state:
            path_to_goal.append(temp_state)
            temp_state = temp_state.last_node
            if not temp_state:
                break
        path_to_goal.reverse()
        for i in path_to_goal:
            i.print()

        print(f"Complexity in time: {len(self.closed)}")
        print(f"Complexity in size: {len(self.closed) + len(self.opened)}")
        print(f"Number of moves: {len(path_to_goal) - 1}")
        print(f"Solving time: {self.solving_time}")

    def solve(self):
        if self.is_solvable():
            print("is solvable")
            try:
                t1 = datetime.datetime.now()
                initial_state = State(self.initial_data)
                initial_state.fval = self.f(initial_state)
                if initial_state.data == self.goal_data:
                    self.goal_state = initial_state
                    self.solving_time = 0
                    return
                heappush(self.opened, initial_state)
                self.opened_hash[initial_state.oneline_data] = initial_state
                while len(self.opened) > 0:
                    current_state = heappop(self.opened)
                    self.closed.add(current_state.oneline_data)
                    for state in current_state.expand():
                        if state.data == self.goal_data:
                            self.goal_state = state
                            t2 = datetime.datetime.now()
                            self.solving_time = t2 - t1
                            return
                        if state.oneline_data in self.closed:
                            continue
                        if state.oneline_data in self.opened_hash:
                            e = self.opened_hash[state.oneline_data]
                            if state.level < e.level:
                                e.fval = self.f(state)
                                e.last_node = state.last_node
                                e.level = state.level
                                e.fval = state.fval
                        else:
                            state.fval = self.f(state)
                            heappush(self.opened, state)
                            self.opened_hash[state.oneline_data] = state
            except MemoryError as e:
                raise Exception('*', f"Oops... Can`t solve Puzzle because of memory error")
        else:
            raise Exception('*', f"is not solvable")



