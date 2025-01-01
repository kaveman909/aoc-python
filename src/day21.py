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
# print(get_shortest_path_dirs(graph_numeric, '7', 'A'))
# print(get_shortest_path_dirs(graph_numeric, 'A', '7'))

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
# print(get_shortest_path_dirs(graph_dir, 'A', '<'))
# print(get_shortest_path_dirs(graph_dir, '<', 'A'))

# Robot using numeric keypad
# for code in codes
code = ['A'] + codes[0]
moves = []
for i in range(len(code) - 1):
  src = code[i]
  dst = code[i + 1]
  moves.append(get_shortest_path_dirs(graph_numeric, src, dst))

flat_moves = flatten_moves(moves)
for move in flat_moves:
  print("".join(move))
print("****************")

# 1st robot using directional keypad
# for move in flat_moves:
move = ['A'] + flat_moves[2]
moves1 = []
for i in range(len(move) - 1):
  src = move[i]
  dst = move[i + 1]
  moves1.append(get_shortest_path_dirs(graph_dir, src, dst))

flat_moves1 = flatten_moves(moves1)
for move in flat_moves1:
  print("".join(move))
print("****************")

# 2nd robot using directional keypad
# for move in flat_moves1:
move = ['A'] + flat_moves1[25]
moves2 = []
for i in range(len(move) - 1):
  src = move[i]
  dst = move[i + 1]
  moves2.append(get_shortest_path_dirs(graph_dir, src, dst))

flat_moves2 = flatten_moves(moves2)
for move in flat_moves2:
  print("".join(move))
