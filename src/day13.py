#!/opt/homebrew/bin/python3

import numpy as np
import re
import sys
from typing import List, Dict, Tuple


def parse_file(file_path: str) -> List[Dict[str, Tuple[int, int]]]:
  with open(file_path, 'r') as f:
    data = f.read().strip()
  pattern = re.compile(r'(\w+(?: \w+)?): X[+=](\d+), Y[+=](\d+)')
  return [
      {m[0]: (int(m[1]), int(m[2])) for m in pattern.findall(group)}
      for group in data.split("\n\n")
  ]


behaviors = parse_file(sys.argv[1])
tol = 1e-3


def play_game(offset):
  total = 0
  for behavior in behaviors:
    coefs = np.array([[behavior["Button A"][0],
                      behavior["Button B"][0]],
                      [behavior["Button A"][1],
                      behavior["Button B"][1]]])

    consts = np.array([behavior["Prize"][0] + offset,
                      behavior["Prize"][1] + offset])

    soln = np.linalg.solve(coefs, consts)
    is_near_int = np.abs(soln - np.round(soln)) < tol
    is_near_int = is_near_int[0] and is_near_int[1]

    if is_near_int:
      total += 3 * soln[0] + 1 * soln[1]
  return int(total)


print(f"Part 1: {play_game(0)}")
print(f"Part 2: {play_game(10000000000000)}")
