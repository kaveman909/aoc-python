import sys
from numpy import array, where
from networkx import Graph, shortest_path_length

grid = array([[c for c in l.strip()] for l in open(sys.argv[1]).readlines()])
rows, cols = grid.shape
print(grid)
print(f"{rows=}, {cols=}")

s = tuple([int(i[0]) for i in where(grid == "S")])
e = tuple([int(i[0]) for i in where(grid == "E")])

wtrack = where(grid == ".")
tracks = [(int(y), int(x)) for y, x in zip(wtrack[0], wtrack[1])]
tracks.append(s)
tracks.append(e)
print(tracks)

dirs = [(0, 1), (0, -1),
        (1, 0), (-1, 0)]

adj_dict = {}

for track in tracks:
  adj_list = []
  for dir in dirs:
    nbr = tuple(array(track) + array(dir))
    if nbr in tracks:
      ny, nx = nbr
      adj_list.append((int(ny), int(nx)))
  adj_dict[track] = tuple(adj_list)

g = Graph(adj_dict)
print(shortest_path_length(g, s, e))
