#!/usr/bin/python3

import sys
import os.path
from puzzle import Puzzle

puz = Puzzle()
if len(sys.argv) > 1:
    fname = sys.argv[1]
    S = 0
    Slist = []
    if not os.path.isfile(fname):
        print("Oops... File '" + fname + "' doesn't exists or is a folder!")
    else:
        with open(fname, "r") as file:
            if puz.parse_content(file.read()) == 0:
                exit()
else:
    print("Write initial puzzle state:")
    if puz.parse_content(sys.stdin.read()) == 0:
        exit()
print(puz.inputData)
# puz = Puzzle(3)
# puz.solve()