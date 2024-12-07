#!/opt/homebrew/bin/python3

import sys
import numpy as np
from numpy.typing import NDArray
from typing import Set, Tuple, List
import copy
from multiprocessing import Pool, cpu_count
import time
import itertools


def print_grid(grid):
  print("==========")
  for line in grid:
    print("".join(line))
  print("==========")
  time.sleep(0.2)


def rotate_cw(dir) -> NDArray:
  # [x, y] -> [y, -x]
  return np.array([-dir[1], dir[0]])


def find_starting_pos(grid) -> NDArray:
  for y in range(len(grid)):
    for x in range(len(grid[0])):
      if grid[y][x] == "^":
        return np.array([x, y])


def in_bounds(pos, dim):
  return (0 <= pos[0] < dim) and (0 <= pos[1] < dim)


def move(pos: NDArray, dir: NDArray, grid):
  nx, ny = pos + dir
  try:
    if grid[ny][nx] == "#":
      dir = rotate_cw(dir)
      return pos, dir
    else:
      return pos + dir, dir
  except IndexError:
    return pos + dir, dir


def count_walls(grid):
  return np.count_nonzero(grid == "#")


def part2(ob) -> int:
  # reset grid, dir, pos, visited
  grid = copy.deepcopy(starting_grid)
  dir = copy.deepcopy(starting_dir)
  pos = copy.deepcopy(starting_pos)
  visited = set()
  # introduce new obstacle
  x, y = ob
  grid[y][x] = "#"
  # loop until either we exit the grid, or we're trapped in
  # an infinite loop
  while True:
    # Don't need to write the "*" for pt 2 but useful for visual debug
    x, y = pos
    grid[y][x] = "*"
    pos, dir = move(pos, dir, grid)
    if not in_bounds(pos, starting_dim):
      # guard leaves grid, don't count it
      return 0
    loc_sig = (pos[0], pos[1], dir[0], dir[1])
    if loc_sig in visited:
      #print_grid(grid)
      return 1
    visited.add(loc_sig)


lines = [l.strip() for l in open(sys.argv[1]).readlines()]
starting_grid = np.array([[c for c in line] for line in lines])
starting_dir = np.array([0, -1])
starting_pos = find_starting_pos(starting_grid)
# Assume Square
starting_dim = len(starting_grid)

if __name__ == "__main__":
  grid = copy.deepcopy(starting_grid)
  dir = copy.deepcopy(starting_dir)
  pos = copy.deepcopy(starting_pos)

  obs: Set[Tuple[int, int]] = set()

  while True:
    x, y = pos
    grid[y][x] = "*"
    pos, dir = move(pos, dir, grid)
    if not in_bounds(pos, starting_dim):
      break
    x, y = pos
    # Add possible obstacle locations used later for part 2
    obs.add((int(x), int(y)))

  print(f"Part 1: {np.count_nonzero(grid == "*")}")

  # Don't want starting pos to be a viable obstacle location per instructions
  # obs = set(itertools.product(range(len(grid)), repeat=2))
  obs.discard((starting_pos[0], starting_pos[1]))

  with Pool(cpu_count()) as pool:
    results: List[int] = pool.map(part2, obs)

  print(f"Part 2: {results.count(1)}")

  # That's not the right answer; your answer is too low.
  # Part 2: 2134, 2135, 2136
  # That's not the right answer (not sure if high or low):
  # 2261 ( "0 <" bug), 2269, 2270
  # Right answer, 2262, but not sure why...
