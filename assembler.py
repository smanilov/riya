def syntax_check(args, lines):
    # TODO
    return lines

def is_label(line):
    if not line.endswith(':'):
        return False
    line = line[:-1]
    return line.isupper()


def get_label(line):
    """Returns the label string of a label declaration. Does not check that the
    given string is indeed a label declaration or not."""
    return line[:-1]


def map_labels(args, lines):
    """Pass through the input lines once and create a map from label names to
    the offset in number of bytes from the first instruction of the input. This
    assumes that each instruction is 4 bytes long."""
    offset = 0
    result = {}
    for line in lines:
        if is_label(line):
            result[get_label(line)] = offset
        else:
            offset += 4

    if (args.debug):
        print("Labels map:", result)

    return result


def assemble(args, lines):
    """Converts the given list of RISC-V assembly lines into a list of RISC-V
    machine codes, one for each line. Each machine code is a string containing
    the machine code in hexadecimal representation (8 hex digits, no separation,
    no new lines).

    Returns None on failure."""
    lines = syntax_check(args, lines)
    if lines is None:
        return None

    labels_map = map_labels(args, lines)

    return lines
