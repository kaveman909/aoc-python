#!/opt/homebrew/bin/python3

import sys
import numpy as np
import re

XMAS = "XMAS"

total = 0
lines = np.array([[c for c in line.strip()] for line in open(sys.argv[1]).readlines()])

def nbox(lines, start, xbox):
  if (start + len(xbox)) <= len(lines):
    return lines[start:start + len(xbox)]
  else:
    return None

def process_line(line):
  s = "".join(line)
  return len(re.findall(XMAS, s))

for i in range(4):
  for line in lines:
    total += process_line(line)
  for i in range(-len(lines) + 1, len(lines)):
    line = np.diag(lines, i)
    total += process_line(line)
  lines = np.rot90(lines)

print(f"Part 1: {total}")

xbox = np.array([["M", ".", "M"],
                 [".", "A", "."],
                 ["S", ".", "S"]])

inter = 0
for _ in range(4):
  i = 0
  while (nline := nbox(lines, i, xbox)) is not None:
    matches = []
    for x, n in zip(xbox, nline):
      matches.append([m.span()[0] for m in re.finditer(f"(?=({''.join(x)}))", "".join(n))])
    inter += len(set(matches[0]) & set(matches[1]) & set(matches[2]))
    i += 1
  xbox = np.rot90(xbox)

print(f"Part 2: {inter}")
