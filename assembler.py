opcodes = ["NOP", "HLT", "ADD", "SUB", "OR",  "NOR", "AND", "XOR", "RSH", "LDI", "ADI", "JMP", "BRH"]
flags = ["Z", "C", "V", "N"]
pseudo_flags = ["=", ">=", "V", "N"]

output = []

with open("input.txt", 'r', encoding='utf-8') as file:
    for line in file:
        line = line.split("//")[0].rstrip()
        if line == "":
            continue
        line = line.split()
        opcode = line[0]
        if opcode in opcodes:
            opcode_number = opcodes.index(opcode)
        if opcode == "HLT":
            output.append(f"{opcode_number:04b}000000000000")
            break
        elif opcode == "NOP":
            output.append("0000000000000000")
        elif opcode == "JMP":
            address = int(line[1])
            output.append(f"{opcode_number:04b}000{address:09b}")
        elif opcode == "BRH":
            if line[1] in pseudo_flags:
                flag = pseudo_flags.index(line[1])
            else:
                flag = flags.index(line[1])
            address = int(line[2])
            output.append(f"{opcode_number:04b}0{flag:02b}{address:09b}")
        elif opcode == "CMP":
            register1 = int(line[1][1:])
            register2 = int(line[2][1:])
            output.append(f"{opcodes.index('SUB'):04b}{register1:04b}{register2:04b}0000")
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
        else:
            register1 = int(line[1][1:])
            register2 = int(line[2][1:])
            register3 = int(line[3][1:])
            output.append(f"{opcode_number:04b}{register1:04b}{register2:04b}{register3:04b}")

with open("output.txt", 'w', encoding='utf-8') as file:
    for line in output:
        file.write(f"{line}\n")
