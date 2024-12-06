#!/opt/homebrew/bin/python3

import sys
from typing import List

lines = [l.strip() for l in open(sys.argv[1]).readlines()]

rules_section = True
rules: List[List[int]] = []
updates: List[List[int]] = []

for line in lines:
  if not line:
    rules_section = False
    continue
  elif rules_section:
    rules.append([int(n) for n in line.split("|")])
  else:
    updates.append([int(n) for n in line.split(",")])

invalid_updates: List[List[int]] = []
for update in updates:
  for rule in rules:
    try:
      left = update.index(rule[0])
      right = update.index(rule[1])
      if left > right:
        invalid_updates.append(update)
        break
    except ValueError:
      pass

updates_tup = [tuple(u) for u in updates]
invalid_updates_tup = [tuple(i) for i in invalid_updates]

valid_updates = set(updates_tup) ^ set(invalid_updates_tup)
total = 0
for update in valid_updates:
  total += update[int(len(update) / 2)]

print(f"Part 1: {total}")

# Re-validify invalid updates
# Basically bubble sort :(
# Improvement idea:
# - Create a dummy "update" that includes each of the unique values from all rules
# - Sort this full update probably using bubble sort
# - Then, create a map to the indices. E.g. if [54, 32, 12], then {54: 0, 32: 1, 12: 2, ...}
# - Pass through all "real" updates once and convert to ordinals, so [32, 12, 54] -> [1, 2, 0]
# - Pt 1: simply check if the update is sorted using a linear "is_sorted()" function
#   - e.g. all(l[i] <= l[i+1] for i in range(len(l) - 1))
# - Pt 2: in same loop as Pt 1, .sort() and get middle value of the invalid updates
# - Should be much faster than bubble sorting every update
for update in invalid_updates:
  while True:
    invalid = False
    for rule in rules:
      try:
        left = update.index(rule[0])
        right = update.index(rule[1])
        if left > right:
          update[left], update[right] = update[right], update[left]
          invalid = True
      except ValueError:
        pass
    if not invalid:
      break

total = 0
for update in invalid_updates:
  total += update[int(len(update) / 2)]

print(f"Part 2: {total}")
