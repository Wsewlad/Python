#!/usr/bin/env python3

# Usage example: python lab2_2.py 2 3 1
# x = namber of 'la'-s
# y = number of couplets
# z = if 1 song end with '!' else with '.'

import sys

x = int(sys.argv[1])
y = int(sys.argv[2])
z = int(sys.argv[3])

song = 'Everybody sing a song:'
la = ' la'
la2 = '-la'
if (x > 1) :
	la += la2 * (x - 1)
res = song + (la if x > 0 else '') * y + ('!' if z == 1 else '.')
print(res)
