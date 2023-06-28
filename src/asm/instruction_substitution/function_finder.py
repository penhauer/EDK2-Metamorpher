import logging
import regex

from asm.instruction_substitution.instruction import InstructionFactory


class FuncRange:

    def __init__(self, begin: int, end: int) -> None:
        # range is end exclusive i.e.
        # [begin, end) not [begin, end]
        self.begin = begin
        self.end = end


class FunctionFinder:

    def __init__(self, lines: list[str]):
        self.lines = lines

    def find_functions(self) -> list[FuncRange]:
        ln = 0
        ranges = []
        while ln < len(self.lines):
            if self.function_starts(ln):
                frange = self.find_function_range(ln)
                ranges.append(frange)
                ln = frange.end
            else:
                ln += 1
        return ranges

    def function_starts(self, ln: int) -> bool:
        IDENTIFIER_REGEX = r'[a-zA-Z_][a-zA-Z0-9_]+'
        m = regex.fullmatch(fr'^{IDENTIFIER_REGEX}:$', self.lines[ln].rstrip())
        function_header = regex.search(r'@function', self.lines[ln - 1])

        if m is None or function_header is None:
            return False

        # assert line[ln] is not a label
        match = regex.fullmatch(InstructionFactory.LABEL_PATTERN, self.lines[ln + 1].strip())
        assert match is None

        return True

    def find_function_range(self, ln: int) -> FuncRange:
        for i in range(ln, len(self.lines)):
            line = self.lines[i]
            match = regex.fullmatch(r'.ret', line.strip())
            if match is not None:
                return FuncRange(ln, i + 1)
            if regex.match('^.size', line.strip()):
                return FuncRange(ln, i + 1)
        logging.error(''.join(self.lines))
        raise Exception("Bad")
