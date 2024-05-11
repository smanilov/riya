from syntax import is_label_decl, is_r_type, is_mem, is_beq

def translate(args, lines, labels_map):
    """For each of the instructions in lines, generates the equivalent machine
    code and returns the result as a list. The input lines should contain only
    syntactically valid instructions or label declarations. No code is generated
    for labels. The labels_map should map labels to byte offsets in the machine
    code (assuming 4 bytes per instruction)."""
    offset = 0
    result = []
    for line in lines:
        if is_label_decl(line):
            continue

        if is_r_type(line):
            result.append(translate_r_type(line))

        if is_mem(line):
            result.append(translate_mem(line))

        if is_beq(line):
            beq = translate_beq(args, line, offset, labels_map)
            if beq is None:
                if args.skip_errors:
                    continue
                else:
                    return None

            result.append(beq)

        offset += 4

    return result


def translate_reg(arg):
    return int(arg[1:])


def translate_imm_reg(arg):
    [imm, reg] = arg[:-1].split("(", 1)
    return (int(imm), translate_reg(reg))


def translate_r_type(line):
    [op, args] = line.split(" ", 1)
    args = args.split(",")
    args = [arg.strip() for arg in args]
    regs = [translate_reg(arg) for arg in args]
    opcode = 0b0110011
    (f3, f7) = {
        "add": (0b000, 0b0000000),
        "sub": (0b000, 0b0100000),
        "and": (0b111, 0b0000000),
        "or": (0b110, 0b0000000),
    }[op]

    result = f7 << 25 | regs[2] << 20 | regs[1] << 15 | f3 << 12 | regs[0] << 7 | opcode
    return "%0.8X" % result


def translate_mem(line):
    [op, args] = line.split(" ", 1)
    args = args.split(",")
    args = [arg.strip() for arg in args]
    r0 = translate_reg(args[0])
    (imm, rs1) = translate_imm_reg(args[1])
    opcode = {
        "lw": 0b0000011,
        "sw": 0b0100011,
    }[op]
    f3 = 0b010

    result = 0
    if op == "lw":
        result = imm << 20 | rs1 << 15 | f3 << 12 | r0 << 7 | opcode
    else:
        imm_h = imm >> 5
        imm_l = imm & 0b11111
        result = imm_h << 25 | r0 << 20 | rs1 << 15 | f3 << 12 | imm_l << 7 | opcode

    return "%0.8X" % result


def translate_beq(program_args, line, offset, labels_map):
    [op, args] = line.split(" ", 1)
    args = args.split(",")
    args = [arg.strip() for arg in args]
    rs1 = translate_reg(args[0])
    rs2 = translate_reg(args[1])
    label = args[2]

    if not label in labels_map:
        prefix = "error:"
        if args.skip_errors:
            prefix = "warning:"
        print(prefix, "no declaration for label %s" % label)
        return None

    imm = labels_map[label] - offset

    if program_args.debug:
        print("label in instruction [%s] computes to offset diff %d" % (line, imm))

    opcode = 0b1100011
    f3 = 0b000

    # imm_h = imm[12 | 10:5]
    imm_h = ((imm >> 12 & 0b1) << 6) | (imm >> 5 & 0b111111)
    # imm_l = imm[4:1|11]
    imm_l = ((imm >> 1 & 0b1111) << 1) | (imm >> 11 & 0b1)
    result = imm_h << 25 | rs2 << 20 | rs1 << 15 | f3 << 12 | imm_l << 7 | opcode

    return "%0.8X" % result
