usage: 
Note: this is a yocto assembler, because it can only assemble a very limited set
of assembly instructions: add, sub, and, or, lw, sw, and beq. The format for
these instructions is as follows:

add rd, rs, r2:    R[rd] = R[rs1] + R[rs2]
sub rd, rs, r2:    R[rd] = R[rs1] - R[rs2]
and rd, rs, r2:    R[rd] = R[rs1] & R[rs2]
or  rd, rs, r2:    R[rd] = R[rs1] | R[rs2]
lw  rd, imm(rs1):  R[rd] = {M[R[rs1] + imm)(31:0)}
sw  rs2, imm(rs1): M[R[rs1] + imm)(31:0) = R[rs2](31:0)
beq rs1, rs2, LABEL: if (R[rs1] == R[rs2]) PC += {imm,1b'0}

These instructions should come one per line and can have a whitespace
indentation, but that's optional. Lines can have comments starting with the #
symbol and continuing until the end of the line. Empty lines (including ones
containing just a comment) are ignored. Lastly, a line could contain a LABEL:
tag, which can be used with a beq instruction to reference the following
instruction as the target of a conditional jump.

If no output file is specified, the output file will have the same relative path
and basename as the input file but with the extension .rvt. The resulting
machine code does not have any prelude or epilogue, but contains just the
instructions written in the input assembly file.

RISC-V yocto assembler

positional arguments:
  file_path             RISC-V assembly file

options:
  -h, --help            show this help message and exit
  --debug               enable debug mode
  -o OUTPUT, --output OUTPUT
                        path to the output file containing the RISC-V machine code
  --dry_run             do not write output
  --skip_errors         skip lines that contain errors
