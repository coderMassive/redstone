import sys

opcodes = ["NOP", "HLT", "ADD", "SUB", "OR",  "NOR", "AND", "XOR", "RSH", "LDI", "ADI", "JMP", "BRH", "CAL", "RET", "MEM"]
flags = ["Z", "C", "V", "N"]
labels = {}
output = []

def process_instruction(line):
    opcode = line[0]
    if opcode in opcodes:
        opcode_number = opcodes.index(opcode)
    if opcode == "NOP":
        output.append("0000000000000000")
    elif opcode == "HLT" or opcode == "RET":
        output.append(f"{opcode_number:04b}000000000000")
    elif opcode == "JMP" or opcode == "CAL":
        address = int(line[1])
        output.append(f"{opcode_number:04b}000{address:09b}")
    elif opcode == "BRH":
        negate = "0"
        if line[1].startswith("!"):
            negate = "1"
            line[1] = line[1][1:]
        flag = flags.index(line[1])
        address = int(line[2])
        output.append(f"{opcode_number:04b}{negate}{flag:02b}{address:09b}")
    elif opcode == "CMP":
        register1 = int(line[1][1:])
        register2 = int(line[2][1:])
        output.append(f"{opcodes.index('SUB'):04b}{register1:04b}{register2:04b}0000")
    elif opcode == "MEM":
        register1 = int(line[1][1:])
        register2 = int(line[2][1:])
        setting = int(line[3])
        output.append(f"{opcode_number:04b}{register1:04b}{register2:04b}{setting:04b}")
    elif opcode == "LDI" or opcode == "ADI":
        register = int(line[1][1:])
        value = int(line[2])
        output.append(f"{opcode_number:04b}{register:04b}{value:08b}")
    elif opcode == "INC":
        register = int(line[1][1:])
        output.append(f"{opcodes.index('ADI'):04b}{register:04b}00000001")
    elif opcode == "DEC":
        register = int(line[1][1:])
        output.append(f"{opcodes.index('ADI'):04b}{register:04b}11111111")
    elif opcode == "RSH":
        register1 = int(line[1][1:])
        register3 = int(line[2][1:])
        output.append(f"{opcode_number:04b}{register1:04b}0000{register3:04b}")
    else: # arithmetic operators
        register1 = int(line[1][1:])
        register2 = int(line[2][1:])
        register3 = int(line[3][1:])
        output.append(f"{opcode_number:04b}{register1:04b}{register2:04b}{register3:04b}")

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
    for line in file:
        line = line.split("//")[0].strip() # remove comments and spaces
        if line == "":
            continue
        line = line.split()
        line = replace_labels(line)
        process_instruction(line)
        
with open("bin/" + sys.argv[1] + ".bin", 'w', encoding='utf-8') as file:
    for line in output:
        file.write(f"{line}\n")
