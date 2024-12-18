#!/opt/homebrew/bin/python3

import sys
from numpy import array, where, ndindex
from numpy.typing import NDArray
from collections import deque
from typing import List


lines = open(sys.argv[1]).readlines()
split = lines.index("\n")
grid = [[c for c in line.strip()] for line in lines[0:split]]
grid2: List[List[str]] = []
for row in range(len(grid)):
  grid2.append([])
  for col in range(len(grid[0])):
    cell = grid[row][col]
    if cell == "O":
      grid2[-1].append("[")
      grid2[-1].append("]")
    elif cell == "@":
      grid2[-1].append(cell)
      grid2[-1].append(".")
    else:
      grid2[-1].append(cell)
      grid2[-1].append(cell)

grid = array(grid)
grid2 = array(grid2)

movements = "".join([line.strip() for line in lines[split + 1:]])
direction_map = {'<': array((0, -1)),
                 'v': array((1, 0)),
                 '>': array((0, 1)),
                 '^': array((-1, 0))}

manual_move_map = {'a': '<',
                   's': 'v',
                   'd': '>',
                   'w': '^'}

bot = array([int(i[0]) for i in where(grid == '@')])


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

#################################################


def is_leftright(view: NDArray):
  return view[1] != 0


def ndarray_in(arr, list_arr):
  return tuple(arr) in [tuple(arr_elem) for arr_elem in list_arr]


def chain(view: NDArray, current: NDArray, grid, locations: List[NDArray]) -> bool:
  next_space = tuple(current + view)
  if (grid[next_space] == "[" or grid[next_space] == "]") and is_leftright(view):
    a = chain(view, current + view, grid, locations)
    if not ndarray_in(current + view, locations):
      locations.append(current + view)
    return a
  elif grid[next_space] == "[":
    a = chain(view, current + view, grid, locations)
    b = chain(view, current + view + direction_map[">"], grid, locations)
    if not ndarray_in(current + view, locations):
      locations.append(current + view)
      locations.append(current + view + direction_map[">"])
    return a and b
  elif grid[next_space] == "]":
    a = chain(view, current + view, grid, locations)
    b = chain(view, current + view + direction_map["<"], grid, locations)
    if not ndarray_in(current + view, locations):
      locations.append(current + view)
      locations.append(current + view + direction_map["<"])
    return a and b
  elif grid[next_space] == "#":
    return False
  elif grid[next_space] == ".":
    return True


bot = array([int(i[0]) for i in where(grid2 == '@')])


for move in movements:
  view = direction_map[move]
  locations: List[NDArray] = []
  should_move = chain(view, bot, grid2, locations)
  if should_move:
    for loc in locations:
      cur_spot = tuple(loc)
      move_spot = tuple(loc + view)
      grid2[move_spot] = grid2[cur_spot]
      grid2[cur_spot] = "."
    # finally, move bot
    grid2[tuple(bot)] = "."
    bot += view
    grid2[tuple(bot)] = "@"

total = 0
for i in ndindex(grid2.shape):
  if grid2[i] == "[":
    total += i[0]*100 + i[1]

print(f"Part 2: {total}")
