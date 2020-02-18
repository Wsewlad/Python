n = 10
nbr = n * n

a = [[0] * n for i in range(n)]

d = "r"

i = 0
j = 0
for k in range(1, nbr):
    if d == "r": # right
        if j < n and a[i][j] == 0: a[i][j] = k
        else: i += 1; j -= 1; d = "d"
    if d == "d": # down
        if i < n and a[i][j] == 0: a[i][j] = k
        else: i -= 1; j -= 1; d = "l"
    if d == "l": # left
        if j >= 0 and a[i][j] == 0: a[i][j] = k
        else: i -= 1; j += 1; d = "u"
    if d == "u": # up
        if i >= 0 and a[i][j] == 0: a[i][j] = k
        else: i += 1; j += 1; d = "r"
    if d == "r": # right
        if j < n and a[i][j] == 0: a[i][j] = k
    if   d == "r": j += 1
    elif d == "d": i += 1
    elif d == "l": j -= 1
    elif d == "u": i -= 1

for i in range(n):
    for j in range(n):
        print("%3d" % a[i][j], end=' ')
    print()