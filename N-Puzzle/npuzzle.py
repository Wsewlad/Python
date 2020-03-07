#!/usr/bin/python3

import sys
import os
import random
import argparse
from puzzle import Puzzle


def get_content(file_name):
    if file_name:
        if not os.path.isfile(file_name):
            raise Exception('*', f"Oops... File '{file_name}' doesn't exists or is a folder!")
        with open(file_name, "r") as file:
            return file.read()
    else:
        print("Write initial puzzle state:")
        return sys.stdin.read()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "-file", help="get input from file (set file name or path). By default reads from stdin")
    parser.add_argument("--h", "-heuristic",
                        help="choose heuristic: mn (manhattan), eu (euclidian), mp (misplaced). Manhattan is default",
                        choices=['mn', 'eu', 'mp'],
                        default='mn')
    parser.add_argument("-r", "-random", help="get random input", action="store_true")

    args = parser.parse_args()
    try:
        if args.r:
            random_file = "inputs/" + random.choice(os.listdir("inputs"))
            print(random_file)
            content = get_content(random_file)
        else:
            content = get_content(args.f)
        puz = Puzzle(content, args.h)
        puz.solve()
        puz.print_result()
    except Exception as e:
        if e.args[0] == '*':
            print(e.args[1])
            exit()
        else:
            raise e
