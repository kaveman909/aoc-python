import sys
from functools import reduce
from numpy import array
from itertools import product
from networkx import Graph, shortest_path_length

coords = [(int(ll[1]), int(ll[0]))
          for l in open(sys.argv[1]).readlines() if (ll := l.strip().split(","))]

my, mx = reduce(lambda x, y: (
    max(x[0], y[0]), max(x[1], y[1])), coords, (0, 0))

grid = array([["."] * (mx + 1) for _ in range((my + 1))])

for i in range(1024):
  grid[coords[i]] = "#"

nodes = product(range(0, my + 1), range(0, mx + 1))

adj_dict = {}

dirs = [(0, 1), (1, 0),
        (0, -1), (-1, 0)]

for node in nodes:
  n_list = []
  if grid[node] == "#":
    continue
  for dir in dirs:
    n = tuple(array(node) + array(dir))
    ny, nx = n
    if 0 <= ny <= my and 0 <= nx <= mx:
      if grid[n] == ".":
        n_list.append((int(ny), int(nx)))
  adj_dict[node] = tuple(n_list)

G = Graph(adj_dict)

print(f"Part 1: {shortest_path_length(G, (0, 0), (my, mx))}")
