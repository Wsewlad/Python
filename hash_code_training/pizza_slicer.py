

import sys
import os.path


if len(sys.argv) > 1:
    fname = sys.argv[1]
    if not os.path.isfile(fname):
        print("Oops... File '" + fname + "' doesn't exists!")
    else:
        file = open(fname, "r")
        infoLine = file.readline().strip().split()
        if not all(x.isdigit() for x in infoLine) or len(infoLine) != 4:
            print("-")
        else:
            print(infoLine)


