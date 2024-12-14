#!/opt/homebrew/bin/python3

import sys
from typing import List, Dict, Tuple

line: List[int] = [int(c) for c in open(sys.argv[1]).readlines()[0].strip()]

gaps = []
gap_indices = []

data = []
data_only = []
for i, d in enumerate(line):
  if i % 2 == 0:
    id = int(i / 2)
    for _ in range(d):
      data_only.append(id)
  else:
    id = -1
    for j in range(d):
      gap_indices.append(j + len(data))
  for j in range(d):
    data.append(id)

data_only.reverse()
data_n = len(data_only)
data_only = data_only[0:len(gap_indices)]

for d, i in zip(data_only, gap_indices):
  data[i] = d

data = data[0:data_n]

checksum = 0
for i, d in enumerate(data):
  checksum += i * d

print(f"Part 1: {checksum}")

#########################################


def find_gaps(data):
  result = {}
  start = None  # Track the start of a range
  for i, value in enumerate(data):
    if value == -1:
      if start is None:  # Start of a new range
        start = i
    else:
      if start is not None:  # End of a range
        result[start] = i - start
        start = None
  if start is not None:  # Handle a range that ends at the last element
    result[start] = len(data) - start
  return result


# idx: len
gaps: Dict[int, int] = {}

# idx: (val, len)
data: Dict[int, Tuple[int, int]] = {}
result: List[int] = []

for i, d in enumerate(line):
  if i % 2 == 0:
    id = int(i / 2)
    data[len(result)] = (id, d)
  else:
    id = -1
    if d > 0:
      gaps[len(result)] = d
  for j in range(d):
    result.append(id)

for data_idx, (data_val, data_len) in reversed(data.items()):
  # find lowest gap_idx that will fit data_len
  # gap_idx can be at most data_idx - 1
  for gap_idx, gap_len in gaps.items():
    if gap_idx > data_idx:
      break
    if gap_len >= data_len:
      for i in range(data_len):
        result[gap_idx + i] = data_val
        result[data_idx + i] = -1
      # We need to recompute gaps
      # NOTE: slower than optimal, we're recomputing all gaps vs just those possibly affected
      # But logic is simple
      gaps = find_gaps(result)
      break

checksum = 0
for i, d in enumerate(result):
  if d > 0:
    checksum += i * d

print(f"Part 2: {checksum}")
