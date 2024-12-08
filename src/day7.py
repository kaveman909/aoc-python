#!/opt/homebrew/bin/python3

import sys
import re
import itertools
from multiprocessing import Pool, cpu_count
from functools import partial

lines = [list(map(int, re.split(r"[\s:]+", l.strip()))) for l in open(sys.argv[1]).readlines()]


def add(x, y):
  return x + y


def mul(x, y):
  return x * y


def concat(x, y):
  return int(str(x) + str(y))


ops_1 = [add, mul]
ops_2 = [add, mul, concat]


def calibrate(line, ops):
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
      return result
  return 0


def calibration_results(ops):
  calibrate_with_ops = partial(calibrate, ops=ops)
  with Pool(cpu_count()) as pool:
    results = pool.map(calibrate_with_ops, lines)
  return sum(results)


if __name__ == "__main__":
  print(f"Part 1: {calibration_results(ops_1)}")
  print(f"Part 2: {calibration_results(ops_2)}")
