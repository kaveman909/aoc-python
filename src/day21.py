import sys
from networkx import DiGraph, all_shortest_paths

codes = [[int(c, 16) for c in l.strip()]
         for l in open(sys.argv[1]).readlines()]


def get_shortest_path_dirs(g, src, dst):

  all_dirs = []
  paths = list(all_shortest_paths(g, source=src, target=dst))

  # Iterate over each path
  for path in paths:
    dirs = []
    for u, v in zip(path, path[1:]):  # Iterate through consecutive node pairs
      dirs.append(g[u][v]['d'])
    all_dirs.append(dirs)
  return all_dirs


# Numeric keypad
# +---+---+---+
# | 7 | 8 | 9 |
# +---+---+---+
# | 4 | 5 | 6 |
# +---+---+---+
# | 1 | 2 | 3 |
# +---+---+---+
#     | 0 | A |
#     +---+---+
adj_dict_numeric = {
    7: {8: {'d': '>'}, 4: {'d': 'v'}},
    8: {7: {'d': '<'}, 5: {'d': 'v'}, 9: {'d': '>'}},
    9: {8: {'d': '<'}, 6: {'d': 'v'}},
    4: {7: {'d': '^'}, 5: {'d': '>'}, 1: {'d': 'v'}},
    5: {4: {'d': '<'}, 8: {'d': '^'}, 6: {'d': '>'}, 2: {'d': 'v'}},
    1: {4: {'d': '^'}, 2: {'d': '>'}},
    2: {1: {'d': '<'}, 5: {'d': '^'}, 3: {'d': '>'}, 0: {'d': 'v'}},
    3: {6: {'d': '^'}, 2: {'d': '<'}, 10: {'d': 'v'}},
    0: {2: {'d': '^'}, 10: {'d': '>'}},
    10: {0: {'d': '<'}, 3: {'d': '^'}}
}
graph_numeric = DiGraph(adj_dict_numeric)
print(get_shortest_path_dirs(graph_numeric, 7, 10))

# Directional keypad
#     +---+---+
#     | ^ | A |
# +---+---+---+
# | < | v | > |
# +---+---+---+
adj_dict_dir = {

}
