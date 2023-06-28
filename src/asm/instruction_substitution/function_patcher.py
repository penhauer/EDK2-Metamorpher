from typing import Callable

from asm.instruction_substitution.function_finder import FunctionFinder, FuncRange


class FunctionPatcher:

    def __init__(self,
                 lines: list[str],
                 function_finder: FunctionFinder,
                 patcher_function: Callable[[list[str]], list[str]]):
        self.lines = lines
        self.function_finder = function_finder
        self.patcher_function = patcher_function

    def patch_all_functions(self):
        ranges = self.function_finder.find_functions()

        # insert empty function range at the beginning
        ranges.insert(0, FuncRange(0, 0))

        # append empty function range at the end
        ranges.append(FuncRange(len(self.lines), len(self.lines)))

        new_lines = []
        for i in range(1, len(ranges)):
            last_range = ranges[i - 1]
            r = ranges[i]
            new_lines.extend(self.lines[last_range.end: r.begin])
            new_lines.extend(self.patcher_function(self.lines[r.begin: r.end]))

        return new_lines
