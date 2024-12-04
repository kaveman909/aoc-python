#!/opt/homebrew/bin/python3

import re
import sys
import functools

lines = functools.reduce(lambda x, y: x.strip() + y, open(sys.argv[1]).readlines(), "")

matches = re.findall(r'mul\((\d+),(\d+)\)', lines)
total = sum([int(m[0]) * int(m[1]) for m in matches])

print(f"Part 1: {total}")

total = 0
on = True

matches = re.findall(r'(do\(\)|don\'t\(\))|mul\((\d+),(\d+)\)', lines)
for match in matches:
  if match[0] == "do()":
    on = True
  elif match[0] == "don't()":
    on = False
  elif on:
    total += int(match[1]) * int(match[2])

print(f"Part 2: {total}")
