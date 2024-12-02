#!/opt/homebrew/bin/python3

import numpy as np
import functools


def remove_at_index(row, i):
  return row[:i] + row[i + 1:]


def valid_internal(row):
  diff = np.diff(row)
  unique = np.unique(np.sign(diff))
  return (len(unique) == 1) and (unique[0] != 0) and (abs(diff.max()) <=3) and (abs(diff.min()) <= 3)


def valid(row, dampen):
  fully_valid = valid_internal(row)
  if fully_valid or not dampen:
    return fully_valid
  # If here, then we are not yet valid, but could be after applying "Problem Dampener"
  for i in range(len(row)):
    if valid_internal(remove_at_index(row, i)):
      return True
  return False


lines = open("../input/day2.txt").readlines()
lines = [[int(x) for x in s.split(" ")] for row in lines if (s := row.strip())]

total = functools.reduce(lambda x, y: x + int(valid(y, False)), lines, 0)
total2 = functools.reduce(lambda x, y: x + int(valid(y, True)), lines, 0)

print(f"Part 1: {total}")
print(f"Part 2: {total2}")
