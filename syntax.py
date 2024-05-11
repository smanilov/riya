def syntax_check(args, lines):
    """Performs a syntax check on the input and prints encountered problems. If
    the args flag "skip_errors" is set, all problematic lines will be skipped
    and reported as warnings. If the flag is not set only the first one will be
    printed as an error, and None will be returned."""
    prefix = "error:"
    if args.skip_errors:
        prefix = "warning:"

    for line in lines:
        if is_label_decl(line):
            continue

        if is_r_type(line):
            continue

        if is_mem(line):
            continue

        if is_beq(line):
            continue

        print(prefix, "unrecognized syntax:", line)
        if not args.skip_errors:
            return None

    return lines


def is_mem(line):
    if line.split(" ", 1)[0] not in ["lw", "sw"]:
        return False

    line = line.split(" ", 1)[1]
    args = line.split(",")
    if len(args) != 2:
        return False

    return is_reg(args[0].strip()) and is_imm_reg(args[1].strip())


def is_beq(line):
    if line.split(" ", 1)[0] != "beq":
        return False

    line = line.split(" ", 1)[1]
    args = line.split(",")
    if len(args) != 3:
        return False

    return (
        is_reg(args[0].strip())
        and is_reg(args[1].strip())
        and is_label(args[2].strip())
    )


def is_label(id):
    return id.isupper()


def is_label_decl(line):
    if not line.endswith(":"):
        return False
    line = line[:-1]
    return is_label(line)


def is_r_type(line):
    if line.split(" ", 1)[0] not in ["add", "sub", "or", "and"]:
        return False

    line = line.split(" ", 1)[1]
    args = line.split(",")
    if len(args) != 3:
        return False

    return (
        is_reg(args[0].strip()) and is_reg(args[1].strip()) and is_reg(args[2].strip())
    )


def is_reg(id):
    if not id[0] == "x":
        return False

    id = id[1:]
    try:
        index = int(id)
        return index >= 0 and index < 32
    except:
        return False


def is_imm_reg(id):
    """Whether the given identifier is an "immediate-register compound", i.e. a
    string of the form imm(reg), e.g. 155(x3). The immediate needs to be a
    12-bit signed integer. No spaces are allowed inside the compound."""
    if id[-1] != ")":
        return False
    if id.find("(") == -1:
        return False

    [imm, reg] = id.split("(", 1)
    reg = reg[:-1]
    if not is_reg(reg):
        return False

    try:
        offset = int(imm)
        return offset >= -2048 and offset < 2048
    except:
        return False
