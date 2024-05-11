# Does mem[2] divide mem[1] evenly?
# memory:
# 0: 0
# 1: x (input)
# 2: y (input)
# 3: x mod y == 0 (output)
# 4: 0x80000000
# 5: 1
# program:
  lw x1, 1(x0)
  lw x2, 2(x0)
  lw x3, 4(x0)
LOOP:
  sub x1, x1, x2
  and x4, x1, x3
  beq x4, x0, LOOP2
  beq x0, x0, FALSE
LOOP2:
  beq x1, x0, TRUE
  beq x0, x0, LOOP
FALSE:
  sw x0, 3(x0)
  beq x0, x0, END
TRUE:
  lw x4, 5(x0)
  sw x4, 3(x0)
END: