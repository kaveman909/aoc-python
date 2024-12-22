import sys
from numpy import array, where
from typing import Tuple, Dict
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


def passthru(d):
  return d


dir_funcs = [(cclkw, 1001), (passthru, 1), (clkw, 1001)]


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
  neighbors = {}
  for i in range(3):
    neighbors[tuple(array(node_k) + dir_funcs[i][0](node_v.dir))
              ] = Node(dir_funcs[i][0](node_v.dir), node_v.dist + dir_funcs[i][1])
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
              from_node_k: Tuple,
              visited: Dict[Tuple, Node]):
  global pt2_counter
  node_v = visited[node_k]
  from_node_v = visited[from_node_k]

  # For each neighbor, walk back if cost is lower
  for _ in range(4):
    neighbor = tuple(array(node_k) + node_v.dir)
    if neighbor in visited:
      counted = False
      # This took far too long to debug! Basically as we're looking for lower
      # costs, we have to consider the cost of turning. Therefor we have to
      # consider a chain of 3 nodes... "from" node, "current" node, and "neighbor" node.
      # - If "from" -> "current" -> "neighbor" create an L (90 deg turn), then we must
      #   componsate this by subtracting 1000
      # - If "from" -> "current" -> "neighbor" creates an | (no turn), then we don't
      #   want to componsate, as we will pick up extraneous nodes.
      if visited[neighbor].dist < node_v.dist:
        counted = True
      else:
        from_dir = tuple(array(node_k) - array(from_node_k))
        neighbor_dir = tuple(array(neighbor) - array(node_k))
        if from_dir != neighbor_dir:
          if visited[neighbor].dist < from_node_v.dist - 1001:
            counted = True
        else:
          if visited[neighbor].dist < from_node_v.dist - 1:
            counted = True

      if counted:
        pt2_counter.add(neighbor)
        walk_back(neighbor, node_k, visited)
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
pt2_counter = set()
walk_back(tuple(end), tuple(end), visited)

print(f"Part 2: {len(pt2_counter) + 1}")
