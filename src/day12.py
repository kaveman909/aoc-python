#!/opt/homebrew/bin/python3

import sys
from typing import List, Tuple, Set
from dataclasses import dataclass
import numpy as np
from itertools import product


@dataclass
class Plot:
  area: int = 0
  perimiter: int = 0
  sides: int = 0
  name: str = ""


def update_sides(coord: Tuple[int, int],
                 dir: Tuple[int, int],
                 plot: Plot,
                 sides: Set[Tuple[int, int, int, int]]):
  # if dir in [(0, 1), (0, -1)], vertical side
  # check (1, 0), (-1, 0) from coord
  side = dir + coord
  row, col = coord
  _, dc = dir
  if dc != 0:
    # vertical side
    above = dir + (row - 1, col)
    below = dir + (row + 1, col)
    if above not in sides and below not in sides:
      plot.sides += 1
  else:
    # horizontal side
    left = dir + (row, col - 1)
    right = dir + (row, col + 1)
    if right not in sides and left not in sides:
      plot.sides += 1
  sides.add(side)


def garden_walk(coord: Tuple[int, int],
                dir: Tuple[int, int],
                visited: Set[Tuple[int, int]],
                plot: Plot,
                sides: Set[Tuple[int, int, int, int]]):
  if coord in visited:
    return
  row, col = coord
  if 0 <= row < rows and 0 <= col < cols:
    # Inside garden
    if str(garden[coord]) == plot.name:
      # In the same plot
      visited.add(coord)
      plot.area += 1
    else:
      # In a new plot, treat like "outside garden"
      plot.perimiter += 1
      update_sides(coord, dir, plot, sides)
      return
  else:
    # Outside garden
    plot.perimiter += 1
    update_sides(coord, dir, plot, sides)
    return

  # If we're here, we're inside garden, and in same plot,
  # so recurse in all directions to find boundaries
  directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
  for direction in directions:
    dr, dc = direction
    garden_walk((row + dr, col + dc), direction, visited, plot, sides)


garden = np.array([[c for c in line.strip()]
                  for line in open(sys.argv[1]).readlines()])
rows, cols = garden.shape
coords = set(product(range(rows), range(cols)))

plots: List[Plot] = []

while coords:
  # Get arbitrary coord from remaining
  coord = coords.pop()
  plot = Plot(name=str(garden[coord]))
  visited = set()
  sides = set()

  garden_walk(coord, None, visited, plot, sides)
  plots.append(plot)

  # filter out already-visited coords
  coords = coords.difference(visited)

total = 0
for plot in plots:
  print(plot)
  total += plot.area * plot.perimiter

print(f"Part 1: {total}")
