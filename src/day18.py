import sys
from functools import reduce

coords = [(int(ll[0]), int(ll[1])) for l in open(sys.argv[1]).readlines() if (ll := l.strip().split(","))]

print(coords)
max_x = reduce(lambda x, y: max(x,y[0]), coords, 0)
max_y = reduce(lambda x, y: max(x,y[1]), coords, 0)


