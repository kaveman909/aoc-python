import sys
from numpy import array, where, array_equal
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
  pos: NDArray
  dir: NDArray
  dist: int = sys.maxsize


def pos_in_node_list(pos: NDArray, node_list: List[Node]):
  for index, node in enumerate(node_list):
    if array_equal(node.pos, pos):
      return index
  return None


def find_min_node(node_list: List[Node]):
  current_min = sys.maxsize
  current_node = None
  for node in node_list:
    if node.dist < current_min:
      current_min = node.dist
      current_node = node
  return current_node


def visit(node: Node,
          visited: List[Node],
          unvisited: List[Node]):

  # Calculate cost to each neighbor
  neighbors = (Node(node.pos + node.dir, node.dir, node.dist + 1),
               Node(node.pos + clkw(node.dir), clkw(node.dir), node.dist + 1001),
               Node(node.pos + cclkw(node.dir), cclkw(node.dir), node.dist + 1001))
  for neighbor in neighbors:
    if maze[tuple(neighbor.pos)] == "#":
      continue
    if pos_in_node_list(neighbor.pos, visited) is not None:
      # No need to visit a node twice
      continue
    node_index = pos_in_node_list(neighbor.pos, unvisited)
    if node_index is None:
      unvisited.append(neighbor)
    else:
      if unvisited[node_index].dist > neighbor.dist:
        unvisited[node_index] = neighbor

  # Finally, mark this node as visited, and remove it from unvisited
  visited.append(node)
  node_index = pos_in_node_list(node.pos, unvisited)
  unvisited.pop(node_index)


maze = array([[c for c in line.strip()]
             for line in open(sys.argv[1]).readlines()])

start: NDArray = array(tuple(w[0] for w in where(maze == "S")))
end: NDArray = array(tuple(w[0] for w in where(maze == "E")))

unvisited: List[Node] = [Node(start, array((0, 1)), 0)]
visited: List[Node] = []

while pos_in_node_list(end, visited) is None:
  node = find_min_node(unvisited)
  visit(node, visited, unvisited)

print(f"Part 1: {visited[pos_in_node_list(end, visited)].dist}")
