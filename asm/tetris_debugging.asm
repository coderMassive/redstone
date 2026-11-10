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
LDI r6 15
LDI r5 0
LDI r7 0

.fall_loop NOP
MEM r2 r1 1 // read piece column
RSH r2 r2

LDI r3 1
AND r2 r3 r4 // check if its on the ground
HLT
OR r4 r5 r5 // save to handle collision after

MEM r3 r6 1 // read stack
AND r2 r3 r4 // check if it collided with stack
OR r4 r7 r7 // save to handle collision after

MEM r2 r1 0 // write piece

DEC r6
DEC r1
BRH !N .fall_loop

CMP r5 r0
BRH !Z .piece_to_stack

RET

.piece_to_stack NOP

LDI r1 7
LDI r2 8

.piece_to_stack_loop NOP
ADD r1 r2 r3 // get stack address for that column
MEM r4 r1 1 // read piece
MEM r5 r3 1 // read stack
OR r4 r5 r6 // new stack
MEM r6 r3 0 // write to stack
MEM r0 r1 0 // clear piece
DEC r1
BRH !N .piece_to_stack_loop

CAL .add_block

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
