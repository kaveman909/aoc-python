#!/opt/homebrew/bin/python3

import functools
import numpy as np

lines = open("../input/day1.txt", newline="").readlines()

locations = np.transpose(np.array([[int(s[0]), int(s[1])] for row in lines if (len(s := row.split("   ")) == 2)])).tolist()
left, right = sorted(locations[0]), sorted(locations[1])
locations = zip(left, right)

total = functools.reduce(lambda x, y: x + abs(y[0] - y[1]), locations, 0)

print(f"Part 1: {total}")

# O(n^2) not great, but works for 1000 elem list
total2 = functools.reduce(lambda x, y: x + (y * right.count(y)), left, 0)

print(f"Part 2: {total2}")
