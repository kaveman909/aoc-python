import sys
from numpy import array, where
from networkx import Graph, shortest_path_length
from multiprocessing import Pool, cpu_count
from itertools import chain
from functools import partial

grid = array([[c for c in l.strip()] for l in open(sys.argv[1]).readlines()])
rows, cols = grid.shape

s = tuple([int(i[0]) for i in where(grid == "S")])
e = tuple([int(i[0]) for i in where(grid == "E")])

wtrack = where(grid == ".")
tracks = [(int(y), int(x)) for y, x in zip(wtrack[0], wtrack[1])]
tracks.append(s)
tracks.append(e)

dirs = [(0, 1), (0, -1),
        (1, 0), (-1, 0)]

cheat_dirs = [(-2, 0), (2, 0), (0, -2), (0, 2),
              (-1, -1), (1, -1), (-1, 1), (1, 1)]

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


def get_path_length(track):
  return (track, shortest_path_length(g, track, e))


def get_time_saved(track, dist_dict):
  ret = []
  for dir in cheat_dirs:
    nbr = tuple(array(track) + array(dir))
    if nbr in tracks:
      t_saved = dist_dict[track] - dist_dict[nbr] - 2
      if t_saved > 0:
        ret.append(t_saved)
  return ret


if __name__ == "__main__":
  with Pool(cpu_count()) as pool:
    dist_dict = {k: v for k, v in pool.map(get_path_length, tracks)}

  get_time_saved_with_dist_dict = partial(get_time_saved, dist_dict=dist_dict)
  with Pool(cpu_count()) as pool:
    ret = chain.from_iterable(pool.map(get_time_saved_with_dist_dict, tracks))
  
  print(f"Part 1: {sum(map(lambda x: x >= 100, ret))}")
