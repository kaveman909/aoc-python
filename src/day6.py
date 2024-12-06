#!/opt/homebrew/bin/python3

import sys
import numpy as np


def rotate_cw(dir):
  # [x, y] -> [y, -x]
  return np.array([-dir[1], dir[0]])


def find_starting_pos(grid):
  for y in range(len(grid)):
    for x in range(len(grid[0])):
      if grid[y][x] == "^":
        grid[y][x] = "*"
        return np.array([x, y])


def inbounds(pos, grid):
  return pos[0] in range(len(grid[0])) and pos[1] in range(len(grid))


def move(pos, dir, grid):
  nx, ny = pos + dir
  try:
    if grid[ny][nx] == "#":
      dir = rotate_cw(dir)
  except IndexError:
    # Let the guard walk out of the grid
    pass
  return pos + dir, dir


lines = [l.strip() for l in open(sys.argv[1]).readlines()]
grid = np.array([[c for c in line] for line in lines])

dir = np.array([0, -1])
pos = find_starting_pos(grid)

while True:
  pos, dir = move(pos, dir, grid)
  if not inbounds(pos, grid):
    break
  x, y = pos
  grid[y][x] = "*"

print(f"Part 1: {np.count_nonzero(grid == "*")}")
