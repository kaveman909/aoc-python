#!/opt/homebrew/bin/python3

import sys
import re

lines = [list(map(int, re.split(r"[\s:]+", l.strip()))) for l in open(sys.argv[1]).readlines()]

print(lines)
