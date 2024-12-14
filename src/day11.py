#!/opt/homebrew/bin/python3

import sys
# from collections import deque

# If the stone is engraved with the number 0, it is replaced by a stone engraved with the number 1.
# If the stone is engraved with a number that has an even number of digits, it is replaced by two stones. The left half of the digits are engraved on the new left stone, and the right half of the digits are engraved on the new right stone. (The new numbers don't keep extra leading zeroes: 1000 would become stones 10 and 0.)
# If none of the other rules apply, the stone is replaced by a new stone; the old stone's number multiplied by 2024 is engraved on the new stone.

stones = [int(s) for s in open(sys.argv[1]).readlines()[0].strip().split(" ")]

def get_new_stones(stones):
  new_stones = []
  for stone in stones:
    if stone == 0:
      new_stones.append(1)
    elif len(str(stone)) % 2 == 0:
      str_stone = str(stone)
      len_stone = len(str_stone)
      new_stones.append(int(str_stone[:int(len_stone/2)]))
      new_stones.append(int(str_stone[int(len_stone/2):]))
    else:
      new_stones.append(stone * 2024)
  
  return new_stones


for _ in range(25):
  stones = get_new_stones(stones)
  
print(f"Part 1: {len(stones)}")
