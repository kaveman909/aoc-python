#!/opt/homebrew/bin/python3

import sys
import numpy as np
import time

def rotate_cw(dir):
  # [x, y] -> [y, -x]
  return np.array([-dir[1], dir[0]])

def convert(c):
  if c == ".":
    return 0
  elif c == "#":
    return -1
  elif c == "^":
    return 1

def find_starting_pos(grid):
  for y in range(len(grid)):
    for x in range(len(grid[0])):
      if grid[y][x] == 1:
        return np.array([x, y])

def inbounds(pos, grid):
  return pos[0] in range(len(grid[0])) and pos[1] in range(len(grid))

def move(pos, dir, grid):
  nx, ny = pos + dir
  try:
    if grid[ny][nx] < 0:
      return pos, rotate_cw(dir)
    else:
      return np.array([nx, ny]), dir
  except IndexError:
    # Let the guard walk out of the grid
    return np.array([nx, ny]), dir

lines = [l.strip() for l in open(sys.argv[1]).readlines()]
grid = np.array([[convert(c) for c in line] for line in lines])

dir = np.array([0, -1])
pos = find_starting_pos(grid)

while True:
  pos, dir = move(pos, dir, grid)
  if not inbounds(pos, grid):
    break
  x, y = pos
  grid[y][x] = 1

print(f"Part 1: {np.count_nonzero(grid == 1)}")
