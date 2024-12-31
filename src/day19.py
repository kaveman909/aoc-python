import sys
from typing import Dict

lines = open(sys.argv[1]).readlines()

patterns = lines[0].strip().split(", ")
designs = [l.strip() for l in lines[2:]]


def check_pattern(design, offset, max_length, cache: Dict[int, int]):
  if offset in cache:
    return cache[offset]
  total = 0
  for length in range(offset, max_length):
    sub_pattern = design[offset:length + 1]
    if sub_pattern in patterns:
      if len(sub_pattern) + offset == max_length:
        total += 1
      else:
        total += check_pattern(design, length + 1, max_length, cache)
  # Only process an offset once
  cache[offset] = total
  return total


total = 0
total2 = 0
for design in designs:
  cache = {}
  ret = check_pattern(design, 0, len(design), cache)
  total += ret > 0
  total2 += ret

print(f"Part 1: {total}")
print(f"Part 2: {total2}")
