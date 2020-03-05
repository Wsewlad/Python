#!/usr/bin/python3

import sys
import os.path
from puzzle import Puzzle


def get_content():
    if len(sys.argv) > 1:
        fname = sys.argv[1]
        if not os.path.isfile(fname):
            raise Exception('*', f"Oops... File '{fname}'  doesn't exists or is a folder!")
        with open(fname, "r") as file:
            return file.read()
    else:
        print("Write initial puzzle state:")
        return sys.stdin.read()


if __name__ == '__main__':
    try:
        content = get_content()
        puz = Puzzle()
        puz.parse_content(content)
    except Exception as e:
        if e.args[0] == '*':
            print(e.args[1])
            exit()
        else:
            raise e

    print(puz.initial_data)
    puz.generate_goal_data()
    print(puz.is_solvable())
    if puz.is_solvable():
        puz.solve()