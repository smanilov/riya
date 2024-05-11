  lw x2, 1(x0)     # assume memory at address 1 contains 1
  lw x3, 2(x0)     # assume memory at address 2 contains 10
  add x1, x0, x0   # x1 = 0
LOOP:
  add x1, x1, x2   # x1 += 1
  beq x1, x3, END
  beq x0, x0, LOOP
END: