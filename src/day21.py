import sys
from networkx import DiGraph, all_shortest_paths
from itertools import product

codes = [[c for c in l.strip()]
         for l in open(sys.argv[1]).readlines()]


def get_shortest_path_dirs(g, src, dst):

  all_dirs = []
  paths = list(all_shortest_paths(g, source=src, target=dst))

  # Iterate over each path
  for path in paths:
    dirs = []
    for u, v in zip(path, path[1:]):  # Iterate through consecutive node pairs
      dirs.append(g[u][v]['d'])
    all_dirs.append(dirs + ['A'])
  return all_dirs


def flatten_moves(moves):
    return [sum(comb, []) for comb in product(*moves)]


def get_all_moves(in_move, graph):
  move = ['A'] + in_move
  moves = []
  for i in range(len(move) - 1):
    src = move[i]
    dst = move[i + 1]
    moves.append(get_shortest_path_dirs(graph, src, dst))
  
  return flatten_moves(moves)


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
    '7': {'8': {'d': '>'}, '4': {'d': 'v'}},
    '8': {'7': {'d': '<'}, '5': {'d': 'v'}, '9': {'d': '>'}},
    '9': {'8': {'d': '<'}, '6': {'d': 'v'}},
    '4': {'7': {'d': '^'}, '5': {'d': '>'}, '1': {'d': 'v'}},
    '5': {'4': {'d': '<'}, '8': {'d': '^'}, '6': {'d': '>'}, '2': {'d': 'v'}},
    '6': {'9': {'d': '^'}, '5': {'d': '<'}, '3': {'d': 'v'}},
    '1': {'4': {'d': '^'}, '2': {'d': '>'}},
    '2': {'1': {'d': '<'}, '5': {'d': '^'}, '3': {'d': '>'}, '0': {'d': 'v'}},
    '3': {'6': {'d': '^'}, '2': {'d': '<'}, 'A': {'d': 'v'}},
    '0': {'2': {'d': '^'}, 'A': {'d': '>'}},
    'A': {'0': {'d': '<'}, '3': {'d': '^'}}
}
graph_numeric = DiGraph(adj_dict_numeric)

# Directional keypad
#     +---+---+
#     | ^ | A |
# +---+---+---+
# | < | v | > |
# +---+---+---+
adj_dict_dir = {
    '^': {'A': {'d': '>'}, 'v': {'d': 'v'}},
    'A': {'^': {'d': '<'}, '>': {'d': 'v'}},
    '<': {'v': {'d': '>'}},
    'v': {'<': {'d': '<'}, '^': {'d': '^'}, '>': {'d': '>'}},
    '>': {'v': {'d': '<'}, 'A': {'d': '^'}}
}
graph_dir = DiGraph(adj_dict_dir)

# Robot using numeric keypad
# for code in codes
flat_moves = get_all_moves(codes[0], graph_numeric)
for move in flat_moves:
  print("".join(move))
print("****************")

# 1st robot using directional keypad
# for move in flat_moves:
flat_moves1 = get_all_moves(flat_moves[2], graph_dir)
for move in flat_moves1:
  print("".join(move))
print("****************")

# 2nd robot using directional keypad
# for move in flat_moves1:
flat_moves2 = get_all_moves(flat_moves1[25], graph_dir)
for move in flat_moves2:
  print("".join(move))
print("****************")
