import sys
from networkx import DiGraph, all_shortest_paths
from itertools import product
from functools import cache

codes = [[c for c in l.strip()]
         for l in open(sys.argv[1]).readlines()]

@cache
def get_shortest_path_dirs(gk, src, dst):

  all_dirs = []
  paths = list(all_shortest_paths(graph_dict[gk], source=src, target=dst))

  # Iterate over each path
  for path in paths:
    dirs = []
    for u, v in zip(path, path[1:]):  # Iterate through consecutive node pairs
      dirs.append(graph_dict[gk][u][v]['d'])
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

# Setup map for graphs to use with caching
graph_dict = {
  0: graph_numeric,
  1: graph_dir
}

# Robot using numeric keypad
complexities = []
for code in codes:
  flat_moves = get_all_moves(code, 0)

  final_move_min = 1_000_000
  for move1 in flat_moves:
    # 1st robot using directional keypad
    flat_moves1 = get_all_moves(move1, 1)
    for move2 in flat_moves1:
      # 2nd robot using directional keypad
      flat_moves2 = get_all_moves(move2, 1)
      final_move_min = min(final_move_min, min(map(len, flat_moves2)))

  code_int = int("".join(code[:-1]))
  complexities.append(code_int * final_move_min)

print(f"Part 1: {sum(complexities)}")
