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
