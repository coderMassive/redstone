import mcschematic
import sys

with open("bin/" + sys.argv[1] + ".bin", "r") as f:
    lines = [line.strip() for line in f if line.strip()]

schem = mcschematic.MCSchematic()

x = 0
z = 0

for line in lines:
    y = 0
    for bit in line:
        if bit == "1":
            schem.setBlock((x, y, z), "minecraft:repeater")
        elif bit == "0":
            schem.setBlock((x, y, z), "minecraft:light_blue_stained_glass")
        y -= 2

    if z <= -90:
        z = 0
        x -= 2
    else:
        z -= 6

schem.save("schem", sys.argv[1], mcschematic.Version.JE_1_18_2)
