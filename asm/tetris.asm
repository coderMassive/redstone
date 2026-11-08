// init board

// clear
LDI r1 7
.board_clear_loop NOP
MEM r0 r1 0
DEC r1
BRH !N .board_clear_loop

// add a testing pixel
LDI r1 128
LDI r2 3
MEM r1 r2 0



// gameloop
.gameloop NOP
CAL .input
CAL .fall
CAL .display
JMP .gameloop


// use input
.input NOP

LDI r7 23
LDI r1 7
LDI r2 1
MEM r3 r7 1

.input_loop NOP
AND r3 r2 r0
BRH !Z .apply_input
.apply_input_back ADD r2 r2 r2
DEC r1
BRH !N .input_loop

RET

.apply_input NOP
LDI r4 128
MEM r5 r1 1
ADD r5 r4 r5
MEM r5 r1 0
JMP .apply_input_back


// sync the display with the board representation
.display NOP

LDI r1 7
LDI r2 31

.update_display_loop NOP
MEM r3 r1 1
MEM r3 r2 0
DEC r2
DEC r1
BRH !N .update_display_loop

RET



// make everything on the board fall
.fall NOP

LDI r1 7

.fall_loop NOP
MEM r2 r1 1
CAL .column_fall
MEM r2 r1 0
DEC r1
BRH !N .fall_loop

RET



// fall a column while not moving the bottom stack, r2 is our input column
.column_fall NOP

// check if it already ends in a 0
LDI r6 1
AND r2 r6 r0
BRH Z .column_fall_trivial

LDI r7 0 // make counter
ADD r2 r0 r3 // make copy

.column_fall_loop RSH r3 r3

// check parity
AND r3 r6 r0
BRH Z .column_fall_even

// odd
INC r7
JMP .column_fall_loop

// even
.column_fall_even NOP

// find tower top
LDI r3 1
.column_fall_lsh_loop ADD r3 r3 r3
DEC r7
BRH !N .column_fall_lsh_loop
RSH r3 r3

// do the shift
RSH r2 r2
ADD r2 r3 r2
RET

.column_fall_trivial RSH r2 r2
RET
