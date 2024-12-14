#!/opt/homebrew/bin/python3

import sys
from typing import Dict


def add_stones(stone, count, stones):
  if stone not in stones:
    stones[stone] = 0
  stones[stone] += count


def get_new_stones(stones: Dict[int, int]):
  new_stones = {}
  for stone, count in stones.items():
    if stone == 0:
      add_stones(1, count, new_stones)

    elif len(str(stone)) % 2 == 0:
      str_stone = str(stone)
      len_stone = len(str_stone)
      lstone = int(str_stone[:int(len_stone / 2)])
      rstone = int(str_stone[int(len_stone / 2):])
      add_stones(lstone, count, new_stones)
      add_stones(rstone, count, new_stones)

    else:
      add_stones(stone * 2024, count, new_stones)

  return new_stones


stones_init = [int(s)
               for s in open(sys.argv[1]).readlines()[0].strip().split(" ")]

stones = {}
for stone in stones_init:
  add_stones(stone, 1, stones)

for i in range(75):
  stones = get_new_stones(stones)
  if i == 24:
    print(f"Part 1: {sum([v for _, v in stones.items()])}")

print(f"Part 2: {sum([v for _, v in stones.items()])}")
