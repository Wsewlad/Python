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


def find_slice_start(pizza):
    for r in range(0, R):
        for c in range(0, C):
            if len(pizza[r][c]) == 1:
                return {"r": r, "c": c}


def check_ingredients(pizza, last_slice):
    t = 0
    m = 0
    for i in range(last_slice["r1"], last_slice["r2"] + 1):
        for j in range(last_slice["c1"], last_slice["c2"] + 1):
            if pizza[i][j] == 'T':
                t += 1¬
            elif pizza[i][j] == 'M':
                m += 1
    return {"t": t, "m": m}


def set_slice(pizza, last_slice):
    for i in range(last_slice["r1"], last_slice["r2"] + 1):
        for j in range(last_slice["c1"], last_slice["c2"] + 1):
            pizza[i][j] += str(S)


def print_pizza(pizza):
    for row in pizza:
        print(row)


def print_result(Slist):
    print(len(Slist))
    for s in Slist:
        print(s["r1"], s["c1"], s["r2"], s["c2"])


def check_slice_size(r2, c2):
    if r2 < R and c2 < C:
        if (r2 + 1) * (c2 + 1) <= H:
            return True
    return False


def check_place(r2, c2):
    if r2 < R and c2 < C:
        return True
    return False


def find_slice(pizza):
    start = find_slice_start(pizza)
    print("Start:", start)
    last_slice["r2"] = last_slice["r1"] = start["r"]
    last_slice["c2"] = last_slice["c1"] = start["c"]

    print("Init slice:", last_slice)

    if last_slice["r2"] + L < R:
        last_slice["r2"] += L
    elif last_slice["c2"] + L < C:
        last_slice["c2"] += L

    print("First slice:", last_slice)

    tm = check_ingredients(pizza, last_slice)
    while 1:
        print("While loop")
        if check_slice_size(last_slice["r2"] + 1, last_slice["c2"]):
            last_slice["r2"] += 1
            print("Row added")
        elif check_slice_size(last_slice["r2"], last_slice["c2"] + 1):
            last_slice["c2"] += 1
            print("Column added")
        else:
            break
        print(tm)
        tm = check_ingredients(pizza, last_slice)

    if tm["t"] >= L and tm["m"] >= L:
        set_slice(pizza, last_slice)
        return True
    return False




if len(sys.argv) > 1:
    fname = sys.argv[1]
    S = 0
    Slist = []
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

            AllIngredients = TCount * MCount
            MinIngredientsInSlice = L * 2
            last_slice = {"r1": 0, "c1": 0, "r2": 0, "c2": 0}

            print("Tomatos:", TCount)
            print("Mushrroms:", MCount)
            print("Min of each ingredient in Slice:", L)
            print("Max ingredients in Slice:", H)
            print("Min ingredients in Slice:", MinIngredientsInSlice)

            while find_slice(pizza):
                S += 1
                Slist.append(last_slice.copy())

            print_pizza(pizza)
            print_result(Slist)




