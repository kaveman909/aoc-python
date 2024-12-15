#!/opt/homebrew/bin/python3

import sys
from typing import Dict, List, Tuple, Set
from dataclasses import dataclass
import numpy as np
from itertools import product


@dataclass
class Plot:
  area: int = 0
  perimiter: int = 0
  name: str = ""


def garden_walk(coord: Tuple[int, int],
                visited: Set[Tuple[int, int]],
                plot: Plot):
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
      return
  else:
    # Outside garden
    plot.perimiter += 1
    return

  # If we're here, we're inside garden, and in same plot,
  # so recurse in all directions to find boundaries
  directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
  for direction in directions:
    dr, dc = direction
    garden_walk((row + dr, col + dc), visited, plot)


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

  garden_walk(coord, visited, plot)
  plots.append(plot)

  # filter out already-visited coords
  coords = coords.difference(visited)

total = 0
for plot in plots:
  total += plot.area * plot.perimiter

print(f"Part 1: {total}")
