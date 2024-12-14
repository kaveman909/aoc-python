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
        visited: Set[Tuple[int, int, int]],
        terminals: Set[Tuple[int, int, int]]) -> None:

  if node in visited:
    return
  visited.add(node)

  if node not in graph:
    terminals.add(node)
    return

  for neighbor in graph[node]:
    dfs(graph, neighbor, visited, terminals)


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
for trailhead in trailheads:
  visited: Set[Tuple[int, int, int]] = set()
  terminals: Set[Tuple[int, int, int]] = set()

  dfs(graph, trailhead, visited, terminals)

  total += count_peaks(terminals)

print(f"Part 1: {total}")
