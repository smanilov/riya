  add x0, x1, x2
SECOND:
  sub x0, x1, x2

  beq x3, x1, SECOND
  # What's up, doc?

  sw x7, 11(x5)
  lw x6, 0(x1) # inline comment works

  # sw x7, 11(x5)

