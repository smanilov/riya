#!/usr/bin/python
from riya import make_parser

f = open("README.txt", "w")
make_parser().print_help(f)
f.close()
