#!/opt/homebrew/bin/python3

import sys
from numpy import array, where, ndindex
from collections import deque

lines = open(sys.argv[1]).readlines()
split = lines.index("\n")
grid = array([[c for c in line.strip()] for line in lines[0:split]])
movements = "".join([line.strip() for line in lines[split + 1:]])

rows, cols = grid.shape

bot = array([int(i[0]) for i in where(grid == '@')])

direction_map = {'<': array((0, -1)),
                 'v': array((1, 0)),
                 '>': array((0, 1)),
                 '^': array((-1, 0))}

for move in movements:
  # look in direction of movement until we hit
  # either a space or a wall
  view = direction_map[move]
  stack = deque()
  next_space = tuple(view + bot)
  while grid[next_space] != "." and grid[next_space] != "#":
    stack.append(grid[next_space])
    next_space = tuple(array(next_space) + view)
  if grid[next_space] == "#":
    continue
  else:
    while not len(stack) == 0:
      grid[next_space] = stack.pop()
      next_space = tuple(array(next_space) - view)
    # at this point back to our original "view" (one step)
    grid[tuple(bot)] = "."
    bot += view
    grid[tuple(bot)] = "@"

total = 0
for i in ndindex(grid.shape):
  if grid[i] == "O":
    total += i[0]*100 + i[1]

print(f"Part 1: {total}")
