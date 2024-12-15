#!/opt/homebrew/bin/python3

import sys
import re
from functools import reduce
from operator import mul


class Bot:
  def __init__(self, px, py, vx, vy):
    self.px = px
    self.py = py
    self.vx = vx
    self.vy = vy

  def move(self):
    self.px = (self.px + self.vx) % xmax
    self.py = (self.py + self.vy) % ymax


bots = [Bot(int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4))) for line in open(
    sys.argv[1]).readlines() if (m := re.match(r"p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)", line.strip()))]

# Assume at least one bot exists at the x and y limits
xmax = reduce(lambda a, b: max(a, b.px), bots, 0) + 1
ymax = reduce(lambda a, b: max(a, b.py), bots, 0) + 1

for _ in range(100):
  for bot in bots:
    bot.move()

quad_bots = [0] * 4
x_mid, y_mid = xmax // 2, ymax // 2

for bot in bots:
  if bot.px == x_mid or bot.py == y_mid:
    continue
  quad_bots[(bot.px > x_mid) + 2 * (bot.py > y_mid)] += 1

print(reduce(mul, quad_bots, 1))
