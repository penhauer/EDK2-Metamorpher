#!/usr/bin/env python3

import sys

from asm.pass_handler import asm_morph


if __name__ == '__main__':
    args = sys.argv
    input = args[1]
    output = args[2]
    asm_morph(input, output)

