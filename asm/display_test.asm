.start LDI r1 31
LDI r2 255
MEM r2 r1 0
LDI r4 30
MEM r0 r4 0

LDI r3 1
LDI r7 7
.loop1 RSH r2 r2
MEM r2 r1 0
MEM r3 r4 0
DEC r4
DEC r7
BRH !Z .loop1

LDI r1 24
LDI r2 1
LDI r4 31
LDI r7 7
.loop2 ADD r2 r2 r2
ADD r2 r3 r2
MEM r2 r1 0
MEM r0 r4 0
DEC r4
DEC r7
BRH !Z .loop2

LDI r3 128
LDI r4 25
LDI r7 7
.loop3 ADD r2 r2 r2
MEM r2 r1 0
MEM r3 r4 0
INC r4
DEC r7
BRH !Z .loop3

LDI r1 31
LDI r5 128
LDI r6 128
LDI r4 24
LDI r7 6

.loop4 RSH r5 r5
ADD r5 r6 r5
ADD r5 r5 r3
MEM r5 r1 0
MEM r0 r4 0
INC r4
DEC r7
BRH !Z .loop4

JMP .start
