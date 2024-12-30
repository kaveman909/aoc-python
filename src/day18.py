import sys
from functools import reduce

coords = [(int(ll[0]), int(ll[1])) for l in open(sys.argv[1]).readlines() if (ll := l.strip().split(","))]

mx, my = reduce(lambda x, y: (max(x[0], y[0]), max(x[1] ,y[1])), coords, (0, 0))
