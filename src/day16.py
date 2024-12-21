import sys
from numpy import array, where, array_equal, set_printoptions
from itertools import product
from typing import Set, Tuple, List, Dict
from numpy.typing import NDArray
from dataclasses import dataclass


def clkw(d):
  # (0, 1) -> (1, 0)
  # (1, 0) -> (0, -1)
  return array((d[1], -d[0]))


def cclkw(d):
  # (0, 1) -> (-1, 0)
  # (-1, 0) -> (0, -1)
  return array((-d[1], d[0]))


@dataclass
class Node:
  dir: NDArray
  dist: int = sys.maxsize


def find_min_node(node_dict: Dict[Tuple, Node]):
  current_min = sys.maxsize
  current_node = None
  for node_k, node_v in node_dict.items():
    if node_v.dist < current_min:
      current_min = node_v.dist
      current_node = node_k
  return current_node


def visit(node_k: Tuple,
          visited: Dict[Tuple, Node],
          unvisited: Dict[Tuple, Node]):

  # Calculate cost to each neighbor
  node_v = unvisited[node_k]
  neighbors = {tuple(array(node_k) + node_v.dir): Node(node_v.dir, node_v.dist + 1),
               tuple(array(node_k) + clkw(node_v.dir)): Node(clkw(node_v.dir), node_v.dist + 1001),
               tuple(array(node_k) + cclkw(node_v.dir)): Node(cclkw(node_v.dir), node_v.dist + 1001)}
  for neighbor_k, neighbor_v in neighbors.items():
    if maze[neighbor_k] == "#":
      continue
    if neighbor_k in visited:
      # No need to visit a node twice
      continue
    if neighbor_k not in unvisited:
      unvisited[neighbor_k] = neighbor_v
    else:
      if unvisited[neighbor_k].dist > neighbor_v.dist:
        unvisited[neighbor_k] = neighbor_v

  # Finally, mark this node as visited, and remove it from unvisited
  visited[node_k] = node_v
  unvisited.pop(node_k)


def walk_back(node_k: Tuple,
              visited: Dict[Tuple, Node]):
  global pt2_counter
  node_v = visited[node_k]

  # For each neighbor, walk back if cost is lower
  for _ in range(4):
    neighbor = tuple(array(node_k) + node_v.dir)
    if neighbor in visited:
      if visited[neighbor].dist < node_v.dist:
        pt2_counter += 1
        walk_back(neighbor, visited)
    node_v.dir = clkw(node_v.dir)


maze = array([[c for c in line.strip()]
             for line in open(sys.argv[1]).readlines()])

start: NDArray = array(tuple(w[0] for w in where(maze == "S")))
end: NDArray = array(tuple(w[0] for w in where(maze == "E")))

unvisited: Dict[Tuple, Node] = {tuple(start): Node(array((0, 1)), 0)}
visited: Dict[Tuple, Node] = {}

while len(unvisited) != 0:
  node = find_min_node(unvisited)
  visit(node, visited, unvisited)

print(f"Part 1: {visited[tuple(end)].dist}")

# Starting at the "E", go to each neighbor that has a lower cost
# Recurse until all lowest-cost paths reach the "S"
pt2_counter = 0
walk_back(tuple(end), visited)
print(pt2_counter)
