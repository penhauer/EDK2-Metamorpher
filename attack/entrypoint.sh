#!/bin/sh
sudo sysctl kernel.randomize_va_space=0
gcc code.c -S --no-stack-protector
./src/morpher.py ./code.s ./morphed.s
gcc code.s -o code
gcc morphed.s -o morphed
exec /bin/bash -l
