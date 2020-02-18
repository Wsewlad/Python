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
        puz.parse_input_file(fname)


# puz = Puzzle(3)
# puz.solve()