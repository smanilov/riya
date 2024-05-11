FIRST:
hello x1, x2, x3
Second:
mux x1, x2, x3
ber x1, x2, FIRST
beq x1, x2, SECOND # accepted; syntax correct; semant wrong
add x32, x1, x3
sub x-1, x0, x2
lw x1, -2049(x2)
sw x7, 1000(x6) # accepted, 1000 is ok
sw x1, 2049(x2)
sw x1, 10000(x2)
