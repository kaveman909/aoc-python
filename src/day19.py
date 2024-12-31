import sys

lines = open(sys.argv[1]).readlines()

patterns = lines[0].strip().split(", ")
print(patterns)

designs = [l.strip() for l in lines[2:]]
print(designs)
