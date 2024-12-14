#!/opt/homebrew/bin/python3

import sys
from typing import List, Tuple, Dict, Set
import itertools
import numpy as np
from numpy.typing import NDArray
import functools


def populate_graph(grid: NDArray,
                   graph: Dict[Tuple[int, int, int], List[Tuple[int, int, int]]],
                   trailheads: List[Tuple[int, int, int]],
                   row: int,
                   col: int):
  directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
  val = int(grid[row, col])
  key = (row, col, val)

  for dr, dc in directions:
    r, c = row + dr, col + dc
    if 0 <= r < rows and 0 <= c < cols:
      nval = int(grid[r, c])
      if val == nval - 1:
        if key not in graph:
          graph[key] = []
        graph[key].append((r, c, nval))
        if key not in trailheads and val == 0:
          trailheads.append(key)


def dfs(graph: Dict[Tuple[int, int, int], List[Tuple[int, int, int]]],
        node: Tuple[int, int, int],
        terminals: Set[Tuple[int, int, int]]) -> None:

  if node not in graph:
    terminals.add(node)
    if node[2] == 9:
      return 1
    return 0

  total = 0
  for neighbor in graph[node]:
    total += dfs(graph, neighbor, terminals)
  
  return total


def count_peaks(terminals: Set[Tuple[int, int, int]]) -> int:
  return functools.reduce(lambda x, y: x + 1 if y[2] == 9 else x, terminals, 0)


grid = np.array([[int(c) for c in line.strip()]
                for line in open(sys.argv[1]).readlines()])

rows, cols = grid.shape

graph: Dict[Tuple[int, int, int], List[Tuple[int, int, int]]] = {}
trailheads: List[Tuple[int, int, int]] = []

coords = itertools.product(range(rows), range(cols))

for row, col in coords:
  populate_graph(grid, graph, trailheads, row, col)

total: int = 0
total2: int = 0
for trailhead in trailheads:
  terminals: Set[Tuple[int, int, int]] = set()

  total2 += dfs(graph, trailhead, terminals)
  total += count_peaks(terminals)

print(f"Part 1: {total}")
print(f"Part 2: {total2}")
