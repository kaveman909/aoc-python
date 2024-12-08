#!/opt/homebrew/bin/python3

import sys
import re
import itertools
from multiprocessing import Pool, cpu_count
from functools import partial
from typing import Match, Dict, Set, Tuple, List
import numpy as np


def in_bounds(an):
  return 0 <= an[0] < dim_x and 0 <= an[1] < dim_y


lines: List[List[str]] = [[c for c in l.strip()] for l in open(sys.argv[1]).readlines()]
dim_y, dim_x = (len(lines), len(lines[0]))

map: Dict[str, Set[Tuple[int, int]]] = {}
antinodes: Set[Tuple[int, int]] = set()

for y in range(len(lines)):
  for x in range(len(lines[0])):
    if m := re.match("[a-zA-Z0-9]", lines[y][x]):
      g = m.group(0)
      if g not in map:
        map[g] = set()
      map[g].add((x, y))

for _, v in map.items():
  combos = itertools.combinations(v, 2)
  for combo in combos:
    a1 = np.array(combo[0])
    a2 = np.array(combo[1])
    diff = a1 - a2
    an1 = a1 + diff
    an2 = a2 - diff
    for an in [an1, an2]:
      if in_bounds(an):
        antinodes.add(tuple(an))

print(f"Part 1: {len(antinodes)}")

antinodes2: Set[Tuple[int, int]] = set()

for _, v in map.items():
  combos = itertools.combinations(v, 2)
  for combo in combos:
    a1 = np.array(combo[0])
    a2 = np.array(combo[1])
    diff = a1 - a2
    # start at a1, go +diff until oob
    # start at a2, go -diff until oob
    while in_bounds(a1):
      antinodes2.add(tuple(a1))
      a1 += diff
    while in_bounds(a2):
      antinodes2.add(tuple(a2))
      a2 -= diff

print(f"Part 2: {len(antinodes2)}")
