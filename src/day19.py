import sys
from functools import cache

lines = open(sys.argv[1]).readlines()

patterns = lines[0].strip().split(", ")
designs = [l.strip() for l in lines[2:]]

@cache
def check_pattern(design, offset, max_length):
  total = 0
  for length in range(offset, max_length):
    sub_pattern = design[offset:length + 1]
    if sub_pattern in patterns:
      if len(sub_pattern) + offset == max_length:
        total += 1
      else:
        total += check_pattern(design, length + 1, max_length)
  return total


counts = [check_pattern(design, 0, len(design)) for design in designs]

print(f"Part 1: {sum(map(bool, counts))}")
print(f"Part 2: {sum(counts)}")
