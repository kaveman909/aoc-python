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
  global regs
  regs[0] >>= combo(operand)


def bxl(operand):
  global regs
  regs[1] ^= operand


def bst(operand):
  global regs
  regs[1] = combo(operand) & 7


def jnz(operand):
  global ip
  if regs[0] != 0:
    ip = operand - 2


def bxc(_):
  global regs
  regs[1] ^= regs[2]


def out(operand):
  global output
  output.append(str(combo(operand) & 7))


def bdv(operand):
  global regs
  regs[1] = regs[0] >> combo(operand)


def cdv(operand):
  global regs
  regs[2] = regs[0] >> combo(operand)


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

print(f"Part 1: {','.join(output)}")

a_start = 1
for i in range(len(prog)):
  prog_str = ",".join([str(p) for p in prog[len(prog) - i - 1:]])
  a_start -= 1
  a_start <<= 3
  output = []
  while ",".join(output) != prog_str:
    regs = [a_start, 0, 0]
    ip = 0
    output = []
    while ip < len(prog) - 1:
      opcode = prog[ip]
      operand = prog[ip + 1]
      opcodes[opcode](operand)
      ip += 2
    a_start += 1
print(f"Part 2: {a_start - 1}")
