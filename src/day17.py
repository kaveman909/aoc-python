import re
import sys

# Register A: 729
# Register B: 0
# Register C: 0

# Program: 0,1,5,4,3,0

program_input = [line.strip() for line in open(sys.argv[1]).readlines()]

regs = []
for i, r in enumerate(("A", "B", "C")):
  regs.append(int(program_input[i].replace(f"Register {r}: ", "")))

prog = [int(p) for p in program_input[4].replace("Program: ", "").split(",")]

