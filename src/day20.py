import sys
from numpy import array, where
from networkx import Graph, shortest_path_length
from multiprocessing import Pool, cpu_count

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


if __name__ == "__main__":
  with Pool(cpu_count()) as pool:
    dist_dict = {k: v for k, v in pool.map(get_path_length, tracks)}

  t_saved_dict = {}

  for track in tracks:
    for dir in cheat_dirs:
      nbr = tuple(array(track) + array(dir))
      if nbr in tracks:
        t_saved = dist_dict[track] - dist_dict[nbr] - 2
        if t_saved > 0:
          if t_saved not in t_saved_dict:
            t_saved_dict[t_saved] = 1
          else:
            t_saved_dict[t_saved] += 1
  
  total = 0
  for k, v in t_saved_dict.items():
    if k >= 100:
      total += v
  
  print(f"Part 1: {total}")
