#!/opt/homebrew/bin/python3

import sys
import re
import itertools

lines = [list(map(int, re.split(r"[\s:]+", l.strip()))) for l in open(sys.argv[1]).readlines()]


def add(x, y):
  return x + y


def mul(x, y):
  return x * y


def concat(x, y):
  return int(str(x) + str(y))


ops_1 = [add, mul]
ops_2 = [add, mul, concat]


def calibration_results(ops):
  total = 0
  for line in lines:
    result = line[0]
    args = line[1:]
    op_combos = list(itertools.product(ops, repeat=len(args) - 1))
    # [(<function add at 0x1008d89a0>,), (<function mul at 0x1008d94e0>,)]
    for op_combo in op_combos:
      # (<function add at 0x1008d89a0>,)
      for i in range(len(op_combo)):
        # [10, 19]
        if i == 0:
          r = op_combo[i](args[i], args[i + 1])
        else:
          r = op_combo[i](r, args[i + 1])
      if r == result:
        total += result
        break
  return total

print(f"Part 1: {calibration_results(ops_1)}")
print(f"Part 2: {calibration_results(ops_2)}")
