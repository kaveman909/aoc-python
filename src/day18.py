import sys
from functools import reduce
from numpy import array

coords = [(int(ll[1]), int(ll[0])) for l in open(sys.argv[1]).readlines() if (ll := l.strip().split(","))]

my, mx = reduce(lambda x, y: (max(x[0], y[0]), max(x[1] ,y[1])), coords, (0, 0))

grid = array([["."] * (mx + 1) for _ in range((my + 1))])

for i in range(12):
  grid[coords[i]] = "#"
