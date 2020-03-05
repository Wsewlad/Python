#!/usr/bin/python3
import datetime
from state import State
from heapq import heappush, heappop, heapify
from itertools import chain

class Puzzle:
    def __init__(self):
        self.n = 0
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
                raise Exception('*', f"Tile '{tile}' is not in range 0:{self.n ** 2}")
            self.validatedTiles.append(tile)
        return list(map(int, res))



    """
    def __validate_tiles(self, tilesLine):
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
    """

    def parse_content(self, content):
        contentList = list(filter(None, map(str.strip, content.strip().split("\n"))))
        for idx, value in enumerate(contentList):
            if value.split("#")[0].strip().isdigit():
                self.n = int(value.split("#")[0].strip())
                contentList = contentList[idx + 1:]
                break
        else:
            raise Exception('*', "No valid Puzzle size found")

        if len(contentList) < self.n:
            raise Exception('*', "Wrong number of tiles")

        self.notValidatedTiles = [str(i) for i in range(self.n ** 2)]
        for value in contentList:
            if value.strip().startswith("#"):
                continue
            validation_result = self.validate_tiles(value.split("#")[0])
            self.initialData.append(validation_result)
            if len(self.initialData) == self.n:
                break
        if len(self.notValidatedTiles) != len(self.validatedTiles):
            raise Exception('*', "Wrong number of tiles")

    """
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
    """

    def f(self, current):
        return self.h(current) + current.level


    def h(self, current):
        res = 0
        for i in range(self.n):
            for j in range(self.n):
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
            if d == "r":  # right
                if j < self.n and self.goalData[i][j] == 0:
                    self.goalData[i][j] = k
                else:
                    i += 1; j -= 1; d = "d"
            if d == "d":  # down
                if i < self.n and self.goalData[i][j] == 0:
                    self.goalData[i][j] = k
                else:
                    i -= 1; j -= 1; d = "l"
            if d == "l":  # left
                if j >= 0 and self.goalData[i][j] == 0:
                    self.goalData[i][j] = k
                else:
                    i -= 1; j += 1; d = "u"
            if d == "u":  # up
                if i >= 0 and self.goalData[i][j] == 0:
                    self.goalData[i][j] = k
                else:
                    i += 1; j += 1; d = "r"
            if d == "r":  # right
                if j < self.n and self.goalData[i][j] == 0: self.goalData[i][j] = k
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
        for i in range(self.n * self.n - 1):
            for j in range(i + 1, self.n ** 2):
                if line_goal.index(line_input[i]) > line_goal.index(line_input[j]):
                    inv += 1
        return inv

    def is_solvable(self):
        line_input = list(chain.from_iterable(self.initialData))
        line_goal = list(chain.from_iterable(self.goalData))

        inv_count = self.inversions_count(line_input, line_goal)
        check_zero_position = abs(line_input.index(0) // self.n - line_goal.index(0) // self.n) + abs(line_input.index(0) % self.n - line_goal.index(0) % self.n)
        if check_zero_position % 2 == 0 and inv_count % 2 == 0:
            return True
        if check_zero_position % 2 == 1 and inv_count % 2 == 1:
            return True
        return False


    def solve(self):
        initialState = State(self.initialData)
        initialState.fval = self.f(initialState)
        heappush(self.opened, initialState)

        goal_state = None
        print(datetime.datetime.now())
        while len(self.opened) > 0:
            currentState = heappop(self.opened)
            heappush(self.closed, currentState)
            if currentState.data == self.goalData:
                print(len(self.opened))
                goal_state = currentState
                break
            for state in currentState.expand():
                found_states = self.opened + self.closed
                if state.data not in [st.data for st in found_states]:
                    state.fval = self.f(state)
                    heappush(self.opened, state)

        print(datetime.datetime.now())
        tmp = goal_state
        tt = []
        while tmp:
            tt.append(tmp)
            tmp = tmp.last_node
            if not tmp:
                break

        tt.reverse()
        for i in tt:
            i.print()

        print(len(tt))
