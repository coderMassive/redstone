import sys
from time import sleep
import pygame

SQ = 40   # square size in pixels
GAP = 2   # gap between squares
pygame.init()
screen = pygame.display.set_mode((8 * SQ, 8 * SQ))
pygame.display.set_caption("Simulator")

labels = {}
flags = {"Z": 0, "C": 0, "V": 0, "N": 0}
registers = [0]*8
memory = [0]*256
stack = []
clock_delay = 0.001

def process_instruction(line, pc):
    print(line)
    match line[0]:
        case "NOP":
            pass
        case "HLT":
            pygame.quit()
            sys.exit()
        case "ADD":
            a, b = registers[int(line[1][1:])], registers[int(line[2][1:])]
            raw = a + b
            result = raw & 0xFF
            flags["C"] = int(raw > 0xFF)
            flags["V"] = int((~(a ^ b) & (a ^ result) & 0x80) != 0)
            registers[int(line[3][1:])] = result
        case "SUB":
            a, b = registers[int(line[1][1:])], registers[int(line[2][1:])]
            raw = a - b
            result = raw & 0xFF
            flags["C"] = int(a >= b)
            flags["V"] = int(((a ^ b) & (a ^ result) & 0x80) != 0)
            registers[int(line[3][1:])] = result
        case "CMP":
            a, b = registers[int(line[1][1:])], registers[int(line[2][1:])]
            raw = a - b
            result = raw & 0xFF
            flags["C"] = int(a >= b)
            flags["V"] = int(((a ^ b) & (a ^ result) & 0x80) != 0)
            registers[0] = result
        case "OR":
            result = registers[int(line[1][1:])] | registers[int(line[2][1:])]
            flags["C"] = 0
            flags["V"] = 0
            registers[int(line[3][1:])] = result
        case "NOR":
            result = ~(registers[int(line[1][1:])] | registers[int(line[2][1:])]) & 0xFF
            flags["C"] = 0
            flags["V"] = 0
            registers[int(line[3][1:])] = result
        case "AND":
            result = registers[int(line[1][1:])] & registers[int(line[2][1:])]
            flags["C"] = 0
            flags["V"] = 0
            registers[int(line[3][1:])] = result
        case "XOR":
            result = registers[int(line[1][1:])] ^ registers[int(line[2][1:])]
            flags["C"] = 0
            flags["V"] = 0
            registers[int(line[3][1:])] = result
        case "RSH":
            flags["C"] = registers[int(line[1][1:])] & 0x01
            result = (registers[int(line[1][1:])] >> 1) & 0xFF
            flags["V"] = 0
            registers[int(line[2][1:])] = result
        case "LDI":
            registers[int(line[1][1:])] = int(line[2])
        case "ADI":
            a, b = registers[int(line[1][1:])], int(line[2])
            raw = a + b
            result = raw & 0xFF
            flags["C"] = int(raw > 0xFF)
            flags["V"] = int((~(a ^ b) & (a ^ result) & 0x80) != 0)
            registers[int(line[1][1:])] = result
        case "INC":
            a = registers[int(line[1][1:])]
            b = 1
            raw = a + b
            result = raw & 0xFF
            flags["C"] = int(raw > 0xFF)
            flags["V"] = int((~(a ^ b) & (a ^ result) & 0x80) != 0)
            registers[int(line[1][1:])] = result
        case "DEC":
            a = registers[int(line[1][1:])]
            b = 1
            raw = a - b
            result = raw & 0xFF
            flags["C"] = int(a >= b)
            flags["V"] = int(((a ^ b) & (a ^ result) & 0x80) != 0)
            registers[int(line[1][1:])] = result
        case "JMP":
            return int(line[1])
        case "BRH":
            if line[1].startswith("!"):
                if flags[line[1][1]] == 0:
                    return int(line[2])
            else:
                if flags[line[1]] == 1:
                    return int(line[2])
        case "CAL":
            stack.append(pc + 1)
            return int(line[1])
        case "RET":
            return stack.pop()
        case "MEM":
            address = registers[int(line[2][1:])]
            setting = line[3]
            if setting == "0": # write to memory
                memory[address] = registers[int(line[1][1:])]
            else: # read from memory
                registers[int(line[1][1:])] = memory[address]
    try:
        flags["Z"] = int(result == 0)
        flags["N"] = int(result & 0x80)
    except:
        pass
    registers[0] = 0
    print(registers)
    return pc + 1

def display(num1, num2):
    # same layout as before: memory[num2] is the left column, bit 7 is the top row
    screen.fill((40, 40, 40))
    for col, addr in enumerate(range(num2, num1, -1)):
        for row in range(8):
            on = (memory[addr] >> (7 - row)) & 1
            color = (255, 255, 255) if on else (0, 0, 0)
            pygame.draw.rect(screen, color, (col * SQ + GAP, row * SQ + GAP, SQ - 2 * GAP, SQ - 2 * GAP))
    pygame.display.flip()

def read_input():
    # keys 1-8 control bits 0-7 of memory[23], 1 while the key is held
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    keys = pygame.key.get_pressed()
    value = 0
    for bit in range(8):
        if keys[pygame.K_1 + bit]:
            value |= 1 << bit
    memory[23] = value

def replace_labels(line):
    for i, part in enumerate(line):
        if part.startswith("."):
            if i == 0:
                line.pop(i) # remove label from instruction
            else:
                line[i] = labels[part] # replace label with address
    return line

# set labels
with open("asm/" + sys.argv[1] + ".asm", 'r', encoding='utf-8') as file:
    i = 0
    for line in file:
        if line.strip() == "" or line.strip().startswith("//"): # ignore empty and comment lines
            continue
        if line.startswith("."):
            labels[line.split()[0]] = str(i)
        i += 1

# process instructions
with open("asm/" + sys.argv[1] + ".asm", 'r', encoding='utf-8') as file:
    lines = file.readlines()

    # remove empty lines
    for i in range(len(lines))[::-1]:
        line = lines[i]
        line = line.split("//")[0].strip()
        if line == "":
            lines.pop(i)

    pc = 0
    while True:
        line = lines[pc]
        line = line.split("//")[0].strip() # remove comment at the end of line
        line = line.split()
        line = replace_labels(line)
        read_input()
        pc = process_instruction(line, pc)
        display(23, 31)
        sleep(clock_delay)
