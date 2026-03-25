import mcschematic

with open("output.txt", "r") as f:
    lines = [line.strip() for line in f if line.strip()]

schem = mcschematic.MCSchematic()

z = 0
for line in lines:
    x = 0
    y = 0

    for bit in line:
        if bit == "1":
            schem.setBlock((x, y, z), "minecraft:repeater")
        elif bit == "0":
            schem.setBlock((x, y, z), "minecraft:light_blue_stained_glass")

        y -= 2

    z -= 6

schem.save(".", "program", mcschematic.Version.JE_1_18_2)
