#!/opt/homebrew/bin/python3

import sys
import numpy as np
import re

XMAS = "XMAS"

total = 0
lines = np.array([[c for c in line.strip()] for line in open(sys.argv[1]).readlines()])

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

print(total)
