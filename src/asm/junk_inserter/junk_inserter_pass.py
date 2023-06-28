import random

from asm.instruction_substitution.function_finder import FunctionFinder
from asm.instruction_substitution.registers import Registers
from asm.morphing_pass import MorphingPass
from asm.instruction_substitution.function_patcher import FunctionPatcher
from asm.utils import random_label


class JunkInserterPass(MorphingPass):
    J1 = """    pushq   %rax
    pushq   %rdx
    movl	{register}, %eax
    addl	$1, %eax
    imull	{register}, %eax
    cltd
    shrl	$31, %edx
    addl	%edx, %eax
    andl	$1, %eax
    subl	%edx, %eax
    cmpl	$1, %eax
    jne	{label}
    ret
{label}:
    popq    %rdx
    popq    %rax
"""

    def __init__(self, lines: list[str]):
        super().__init__(lines)

    def morph_lines(self) -> list[str]:
        function_finder = FunctionFinder(self.lines)
        function_patcher = FunctionPatcher(
            self.lines,
            function_finder,
            self.morph_function,
        )
        return function_patcher.patch_all_functions()

    def morph_function(self, lines: list[str]) -> list[str]:
        # do insert every 200 instructions
        step = 200
        if len(lines) <= 200:
            return lines

        morphed = lines.copy()
        for i in range(0, len(lines), step):
            ind = i + random.randint(0, min(len(lines) - i, step))
            junk = JunkInserterPass.J1.format(
                register=Registers.get_random_register(32),
                label=random_label(),
            )
            morphed.insert(ind, junk)
        return morphed

