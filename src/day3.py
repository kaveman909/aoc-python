#!/opt/homebrew/bin/python3

import re
import sys

lines = open(sys.argv[1]).readlines()

total = 0
for row in lines:
  matches = re.findall(r'mul\((\d+),(\d+)\)', row)
  total += sum([int(m[0]) * int(m[1]) for m in matches])

print(f"Part 1: {total}")

total = 0
on = True
for row in lines:
  muls = list(re.finditer(r'mul\((\d+),(\d+)\)', row))
  muls_is = [x.span()[0] for x in muls]
  dos = [x.span()[0] for x in re.finditer(r'do\(\)', row)]
  donts = [x.span()[0] for x in re.finditer(r"don't\(\)", row)]
  
  for i in range(len(row)):
    if i in dos:
      on = True
    elif i in donts:
      on = False
    elif (i in muls_is) and on:
      idx = muls_is.index(i)
      total += int(muls[idx].group(1)) * int(muls[idx].group(2))

print(f"Part 2: {total}")
