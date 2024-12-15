#!/opt/homebrew/bin/python3

import sys
import re
from functools import reduce
from operator import mul
import statistics


class Bot:
  def __init__(self, px, py, vx, vy):
    self.px = px
    self.py = py
    self.vx = vx
    self.vy = vy

  def move(self):
    self.px = (self.px + self.vx) % xmax
    self.py = (self.py + self.vy) % ymax

  def render(self, grid):
    grid[self.py][self.px] = "*"


def display_grid(grid):
  print("-" * xmax)
  for line in grid:
    print("".join(line))
  print("-" * xmax)


def get_quadbots(bots):
  quadbots = [0] * 4
  x_mid, y_mid = xmax // 2, ymax // 2

  for bot in bots:
    if bot.px == x_mid or bot.py == y_mid:
      continue
    quadbots[(bot.px > x_mid) + 2 * (bot.py > y_mid)] += 1

  return quadbots


bots = [Bot(int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4))) for line in open(
    sys.argv[1]).readlines() if (m := re.match(r"p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)", line.strip()))]

# Assume at least one bot exists at the x and y limits
xmax = reduce(lambda a, b: max(a, b.px), bots, 0) + 1
ymax = reduce(lambda a, b: max(a, b.py), bots, 0) + 1

for i in range(10000):
  if i == 100:
    print(f"Part 1: {reduce(mul, get_quadbots(bots), 1)}")

  dev = statistics.stdev(get_quadbots(bots))
  # Magic number discovered through iteration
  if dev > 155:
    grid = [[" "] * xmax for _ in range(ymax)]
    for bot in bots:
      bot.render(grid)
    display_grid(grid)
    print(f"Part 2: {i}")

  for bot in bots:
    bot.move()
