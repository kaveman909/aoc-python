#!/opt/homebrew/bin/python3

import re
import functools

left = []
right = []
with open("../input/day1.txt", newline="") as f:
  for row in f.readlines():
    m = re.match(r"(\d+)   (\d+)", row)
    left.append(int(m[1]))
    right.append(int(m[2]))

left = sorted(left)
right = sorted(right)

locations = zip(left, right)

total = functools.reduce(lambda x, y: x + abs(y[0] - y[1]), locations, 0)

print(f"Part 1: {total}")

# O(n^2) not great, but works for 1000 elem list
total2 = functools.reduce(lambda x, y: x + (y * right.count(y)), left, 0)

print(f"Part 2: {total2}")
