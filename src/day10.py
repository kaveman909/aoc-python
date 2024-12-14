#!/opt/homebrew/bin/python3

import sys
from typing import List, Dict, Tuple

lines: List[List[int]] = [[int(c) for c in line.strip()] for line in open(sys.argv[1]).readlines()]

print(lines)
