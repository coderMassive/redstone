// clear
LDI r1 15
.board_clear_loop NOP
MEM r0 r1 0
DEC r1
BRH !N .board_clear_loop

CAL .add_block

// gameloop
.gameloop NOP
CAL .fall
CAL .display
JMP .gameloop

// sync the display with the board representation
.display NOP

LDI r1 7
LDI r2 15
LDI r3 31

.update_display_loop NOP
MEM r4 r1 1 // piece
MEM r5 r2 1 // stack
OR r4 r5 r6 // merge piece and stack
MEM r6 r3 0 // display
DEC r3
DEC r2
DEC r1
BRH !N .update_display_loop

RET

// make everything on the board fall
.fall NOP

LDI r1 7
.fall_loop MEM r2 r1 1
RSH r2 r2
MEM r2 r1 0
DEC r1
BRH !N .fall_loop

RET


// add a new active block
.add_block NOP
LDI r1 64
LDI r2 4
MEM r1 r2 0
LDI r1 192
DEC r2
MEM r1 r2 0
LDI r1 128
DEC r2
MEM r1 r2 0
RET
