// find 5th fib number
LDI r1 5
CAL .fib

// save to ram
LDI r2 0 // address
MEM r1 r2 0

// find 10th fib number
LDI r1 10
CAL .fib

// save to ram
LDI r2 1 // address
MEM r1 r2 0

// reset all registers
LDI r1 0
LDI r2 0
LDI r3 0
LDI r4 0
LDI r5 0
LDI r6 0
LDI r7 0

// load values from ram
LDI r3 0
MEM r1 r3 1
LDI r3 1
MEM r2 r3 1
LDI r3 0 // reset r3

HLT

// fib function, input/output in r1

// check if it is odd or even
.fib RSH r1 r2
ADD r2 r2 r2
SUB r1 r2 r5 // r5 is now r1 % 2

INC r1 // if r1 is even, it will become odd and floor the division making this not matter; if r1 is odd, it will loop an extra time instead of flooring it
RSH r1 r1 // divide by 2, as every loop is 2 numbers

// load first two fib numbers
LDI r2 1
LDI r3 1

LDI r4 1 // 4, count loading the first 2 fib numbers as a run

// calculate next 2 fib numbers
.loop ADD r2 r3 r2
ADD r3 r2 r3

INC r4 // increment loop count

// loop if haven't looped enough times
CMP r4 r1
BRH !C .loop

// check parity of input
CMP r5 r0
BRH Z .even

// odd
ADD r2 r0 r1
JMP .end // skip even

// even
.even ADD r3 r0 r1

.end RET
