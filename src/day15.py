#!/opt/homebrew/bin/python3

import sys
import numpy as np

lines = open(sys.argv[1]).readlines()
split = lines.index("\n")
grid = np.array([[c for c in line.strip()] for line in lines[0:split]])
instructions = "".join([line.strip() for line in lines[split + 1:]])

print(grid)
print(instructions)
