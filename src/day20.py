import sys
from numpy import array, where

grid = array([[c for c in l.strip()] for l in open(sys.argv[1]).readlines()])
rows, cols = grid.shape
print(grid)
print(f"{rows=}, {cols=}")

s = tuple([int(i[0]) for i in where(grid == "S")])
e = tuple([int(i[0]) for i in where(grid == "E")])

wtrack = where(grid == ".")
track = [(int(y), int(x)) for y, x in zip(wtrack[0], wtrack[1])]

print(track)
