from asm.instruction_substitution.instruction_substitution_pass import InstructionSubstitutionPass
from asm.function_permutation.section_permuter import SectionPermutationPass
from asm.junk_inserter.junk_inserter_pass import JunkInserterPass

passes = [
    InstructionSubstitutionPass,
    SectionPermutationPass,
    JunkInserterPass,
]


def do_apply_passes(lines: list[str]) -> list[str]:
    for morphing_pass_class in passes:
        morphing_pass = morphing_pass_class(lines)
        lines = morphing_pass.morph_lines()
    return lines


def asm_morph(input_file: str, output_file: str):
    f = open(input_file)
    lines = f.readlines()
    f.close()
    new_lines = do_apply_passes(lines)
    g = open(output_file, mode='w')
    g.writelines(new_lines)
    g.close()
