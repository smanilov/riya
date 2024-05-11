#!/usr/bin/python
import sys
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="""RISC-V yocto assembler

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
""")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    parser.add_argument("file_path", help="RISC-V assembly file")
    parser.add_argument("-o", "--output", help="Path to the output file"
                        "containing the RISC-V machine code")
    return parser.parse_args()


def read_lines(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            # Remove whitespace from each line
            lines = [line.strip() for line in lines]
            lines = [line.split('#')[0] for line in lines]
            lines = [line for line in lines if len(line) > 0]
        return lines
    except FileNotFoundError:
        print("File not found.")
        return None
    except Exception as e:
        print("An error occurred:", e)
        return None

def debug_stripped(args, input_lines):
    if args.debug:
        print("Assembly stripped from comments and whitespace:")
        for line in lines:
            print(line)


def write_output(args, lines):
    output_file_path = args.file_path.replace(".asm", ".rvt")
    if args.output:
        output_file_path = args.output

    if args.debug:
        print("Output file:", output_file_path)

    f = open(output_file_path, "w")
    lines = [line + "\n" for line in lines]
    f.writelines(lines)


def main():
    args = parse_args()

    lines = read_lines(args.file_path)

    if lines is None:
        return

    debug_stripped(args, lines)

    # lines = assemble(args, lines)

    # debug_assembled(...)

    write_output(args, lines)


if __name__ == "__main__":
    main()
