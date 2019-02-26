import sys
import os.path

"""
Input data:
R C L H

M - mushroom
T - tomato
R - number of rows (1 <= AND <= 1000)
C - number of columns (1 <= AND <= 1000)
L - minimum of each ingredient in Slice (1 <= AND <= 1000)
H - maximum ingredients in Slice (1 <= AND <= 1000)

Output data:
S
r1, c1, r2, c2
... * S

S - number of slices (0 <= AND <= R * C)
0 <= r1, r2 < R
0 <= c1, c2 < C

"""


def find_first_ing(pizza):
    for r in range(0, R):
        for c in range(0, C):
            if len(pizza[r][c]) == 1:
                return [r, c]


#def find_slice(pizzaToSlice):


def set_found_slice(pizza, r1, c1, r2, c2):
    for i in range(r1, r2+1):
        for j in range(c1, c2+1):
            pizza[i][j] += str(S)


def print_pizza(pizza):
    for row in pizza:
        print(row)


if len(sys.argv) > 1:
    fname = sys.argv[1]
    S = 0
    if not os.path.isfile(fname):
        print("Oops... File '" + fname + "' doesn't exists or is a folder!")
    else:
        pizza = []
        with open(fname, "r") as file:
            infoLine = file.readline().strip().split()
            R = int(infoLine[0])
            C = int(infoLine[1])
            L = int(infoLine[2])
            H = int(infoLine[3])

            for r in range(1, R + 1):
                pizza.append(list(file.readline().strip()))

            TCount = sum(x.count('T') for x in pizza)
            MCount = sum(x.count('M') for x in pizza)
            MaxSliceNbr = min(TCount, MCount)
            MidSliceNbr = int((R * C) / MaxSliceNbr)
            print(TCount)
            print(MCount)
            print(MidSliceNbr)

            set_found_slice(pizza, 0, 0, 1, 4)
            S += 1

            print_pizza(pizza)
            print(S)

            print(find_first_ing(pizza))



