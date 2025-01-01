import sys
from numpy import array, where
from networkx import Graph, shortest_path_length
from multiprocessing import Pool, cpu_count
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


def generate_cheat_dirs(d):
  return {(x, y) for x in range(-d, d + 1) for y in range(-d, d + 1) if abs(x) + abs(y) <= d}


def get_path_length(track):
  return (track, shortest_path_length(g, track, e))


def get_time_saved(track, dist_dict, cheat_dir_n):
  ret = 0
  for dir in generate_cheat_dirs(cheat_dir_n):
    nbr = tuple(array(track) + array(dir))
    dy, dx = dir
    if nbr in tracks:
      t_saved = dist_dict[track] - dist_dict[nbr] - (abs(dy) + abs(dx))
      if t_saved >= 100:
        ret += 1
  return ret


if __name__ == "__main__":
  with Pool(cpu_count()) as pool:
    dist_dict = {k: v for k, v in pool.map(get_path_length, tracks)}

  get_time_saved_with_dist_dict = partial(get_time_saved, dist_dict=dist_dict, cheat_dir_n=2)
  with Pool(cpu_count()) as pool:
    ret = sum(pool.map(get_time_saved_with_dist_dict, tracks))

  print(f"Part 1: {ret}")

  get_time_saved_with_dist_dict2 = partial(get_time_saved, dist_dict=dist_dict, cheat_dir_n=20)
  with Pool(cpu_count()) as pool:
    ret = sum(pool.map(get_time_saved_with_dist_dict2, tracks))

  print(f"Part 2: {ret}")
