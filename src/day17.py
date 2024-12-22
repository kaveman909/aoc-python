import sys


def combo(operand):
  if operand == 7:
    print(f"ERROR: combo operand {operand} illegal!")
    exit(1)
  if operand <= 3:
    return operand
  else:
    return regs[operand - 4]


def adv(operand):
  num = regs[0]
  den = 2**combo(operand)
  regs[0] = int(num / den)


def bxl(operand):
  regs[1] ^= operand


def bst(operand):
  regs[1] = combo(operand) % 8


def jnz(operand):
  global ip
  if regs[0] != 0:
    ip = operand - 2


def bxc(_):
  regs[1] ^= regs[2]


def out(operand):
  global output
  output.append(str(combo(operand) % 8))


def bdv(operand):
  num = regs[0]
  den = 2**combo(operand)
  regs[1] = int(num / den)


def cdv(operand):
  num = regs[0]
  den = 2**combo(operand)
  regs[2] = int(num / den)


program_input = [line.strip() for line in open(sys.argv[1]).readlines()]

regs = []
ip = 0
output = []
opcodes = [adv, bxl, bst, jnz, bxc, out, bdv, cdv]

for i, r in enumerate(("A", "B", "C")):
  regs.append(int(program_input[i].replace(f"Register {r}: ", "")))

prog = [int(p) for p in program_input[4].replace("Program: ", "").split(",")]

while ip < len(prog) - 1:
  opcode = prog[ip]
  operand = prog[ip + 1]
  opcodes[opcode](operand)
  ip += 2

print(",".join(output))
