import sys
from functools import reduce

lines = open(sys.argv[1]).readlines()

patterns = lines[0].strip().split(", ")
designs = [l.strip() for l in lines[2:]]


def check_pattern(design, offset, max_length):
  for length in range(offset, max_length):
    sub_pattern = design[offset:length + 1]
    if sub_pattern in patterns:
      if len(sub_pattern) + offset == max_length:
        return True
      if check_pattern(design, length + 1, max_length) is True:
        return True
  return False


print(f"Part 1: {reduce(lambda x, y: x +
      check_pattern(y, 0, len(y)), designs, 0)}")
