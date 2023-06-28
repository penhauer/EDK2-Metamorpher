from asm.instruction_substitution.function_finder import FunctionFinder, FuncRange
from asm.instruction_substitution.function_patcher import FunctionPatcher
from asm.instruction_substitution.instruction_morpher import InstructionMorpherFactory
from asm.instruction_substitution.instruction import InstructionFactory
from asm.morphing_pass import MorphingPass


class InstructionSubstitutionPass(MorphingPass):

    def __init__(self, lines: list[str]):
        super().__init__(lines)
        self.instruction_factory = InstructionFactory()

    def morph_lines(self) -> list[str]:
        function_finder = FunctionFinder(self.lines)
        function_patcher = FunctionPatcher(
            self.lines,
            function_finder,
            self.morph_function,
        )
        return function_patcher.patch_all_functions()

    def morph_function(self, lines: list[str]) -> list[str]:
        if len(lines) <= 10:
            return lines

        imf = InstructionMorpherFactory()
        morphed_lines = []
        for line in lines:
            instruction = self.instruction_factory.get_instruction(line)
            if instruction:
                morpher = imf.get_morpher(instruction)
                morphed = morpher.morph_instruction(instruction)
                morphed_lines.extend(morphed)
            else:
                morphed_lines.append(line)

        return morphed_lines
