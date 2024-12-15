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
tol = 1e-6
total = 0

for behavior in behaviors:
  coefs = np.array([[behavior["Button A"][0],
                    behavior["Button B"][0]],
                   [behavior["Button A"][1],
                    behavior["Button B"][1]]])

  consts = np.array([behavior["Prize"][0],
                     behavior["Prize"][1]])

  soln = np.linalg.solve(coefs, consts)
  is_near_int = np.allclose(soln, np.round(soln), atol=tol)

  if soln[0] <= 100.0 and soln[1] <= 100.0 and is_near_int:
    total += 3 * soln[0] + 1 * soln[1]

print(f"Part 1: {int(total)}")
