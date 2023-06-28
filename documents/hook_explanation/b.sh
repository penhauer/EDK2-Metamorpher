
# Assembly Compilation Flags
"x86_64-linux-gnu-gcc"  -S \
  -c \
  -o output.s \
  -other_flags1 -other_flags2 ...
  -I header_file1 -I header_file2  ... \
  input.c


# Object file Compilation Flags
"x86_64-linux-gnu-gcc" -c \
  -o output.obj \
  -other_flags1 -other_flags2 ...
  -I header_file1 -I header_file2 ... \
  output.s

