import random
import logging
import abc

from asm.instruction_substitution.registers import Registers
from asm.instruction_substitution.instruction import Operand, Instruction

logger = logging.getLogger(__name__)


class SingleInstructionMorpher(abc.ABC):

    @abc.abstractmethod
    def morph_instruction(self, instruction: Instruction) -> list[str]:
        pass


class InstructionMorpherFactory:

    def __init__(self):
        self.identity_instruction_morpher = IdentityInstructionMorpher()
        self.move_instruction_morpher = MoveInstructionMorpher(self.identity_instruction_morpher)
        self.and_instruction_morpher = AndInstructionMorpher(self.identity_instruction_morpher)
        self.xor_instruction_morpher = XorInstructionMorpher(self.identity_instruction_morpher)

    def get_morpher(self, instruction: Instruction) -> SingleInstructionMorpher:
        if instruction.instruction.startswith('mov'):
            return self.move_instruction_morpher
        elif instruction.instruction.startswith('and'):
            return self.and_instruction_morpher
        elif instruction.instruction.startswith('xor'):
            return self.xor_instruction_morpher
        else:
            return IdentityInstructionMorpher()


class IdentityInstructionMorpher(SingleInstructionMorpher):

    def morph_instruction(self, instruction: Instruction):
        return [
            instruction.text
        ]


class MoveInstructionMorpher(SingleInstructionMorpher):

    def __init__(self, identity_morpher: IdentityInstructionMorpher):
        self.identity_morpher = identity_morpher

    def morph_instruction(self, instruction: Instruction) -> list[str]:
        first_operand = instruction.operands[0]
        second_operand = instruction.operands[1]

        if instruction.instruction in [Instruction.MOVQ] and \
                first_operand.type == Operand.OperandType.REGISTER and \
                second_operand.type == Operand.OperandType.REGISTER:
            return [
                f'\tpushq {first_operand.register}\n',
                f'\tpopq {second_operand.register}\n',
            ]
        elif instruction.instruction in [Instruction.MOVB, Instruction.MOVL, Instruction.MOVQ] and \
                first_operand.type == Operand.OperandType.IMMEDIATE_VALUE:
            a, b = value_builder.build_immediate_value(int(first_operand.immediate), instruction.get_bits())
            sz = instruction.instruction[3]
            morphed = [
                f'\t{instruction.instruction} ${a}, {second_operand.text}\n'
                f'\tadd{sz} ${b}, {second_operand.text}\n'
            ]
            return morphed
        elif instruction.instruction == Instruction.MOVZBL:
            return self.identity_morpher.morph_instruction(instruction)
        else:
            return self.identity_morpher.morph_instruction(instruction)


class AndInstructionMorpher(SingleInstructionMorpher):

    def __init__(self, identity_morpher: IdentityInstructionMorpher):
        self.identity_morpher = identity_morpher

    def morph_instruction(self, instruction: Instruction) -> list[str]:
        first_operand = instruction.operands[0]
        second_operand = instruction.operands[1]

        if instruction.instruction in [Instruction.ANDB, Instruction.ANDL, Instruction.ANDQ] and \
                first_operand.type == Operand.OperandType.REGISTER and \
                second_operand.type == Operand.OperandType.REGISTER:
            """
                (b & a) = ~(~b | ~a)

                b &= a
                =
                b ^= -1
                a ^= -1
                b |= a
                b ^= -1
                a ^= -1
            """

            bits = instruction.instruction[3]
            morphed = [
                f'\txor{bits} $-1, {second_operand.text}\n',
                f'\txor{bits} $-1, {first_operand.text}\n',
                f'\tor{bits} {first_operand.text}, {second_operand.text}\n',
                f'\txor{bits} $-1, {second_operand.text}\n',
                f'\txor{bits} $-1, {first_operand.text}\n',
            ]
            if random.randint(0, 1) % 2 == 0:
                morphed[0], morphed[1] = morphed[1], morphed[0]
            if random.randint(0, 1) % 2 == 0:
                morphed[3], morphed[4] = morphed[4], morphed[3]
            return morphed

        elif instruction.instruction in [Instruction.ANDB, Instruction.ANDL, Instruction.ANDQ] and \
                first_operand.type == Operand.OperandType.IMMEDIATE_VALUE:
            bits = instruction.get_bits()
            x = int(first_operand.immediate)
            x_not = value_builder.negate_immediate(x, bits)

            """
                (b & x) = ~(~b | ~x)

                b &= x
                =
                b ^= -1
                b |= ~x
                b ^= -1
            """

            bits = instruction.instruction[3]
            return [
                f'\txor{bits} $-1, {second_operand.text}\n',
                f'\tor{bits} ${x_not}, {second_operand.text}\n',
                f'\txor{bits} $-1, {second_operand.text}\n',
            ]
        else:
            return self.identity_morpher.morph_instruction(instruction)


class XorInstructionMorpher(SingleInstructionMorpher):

    def __init__(self, identity_morpher: IdentityInstructionMorpher):
        self.identity_morpher = identity_morpher

    def morph_instruction(self, instruction: Instruction) -> list[str]:
        first_operand = instruction.operands[0]
        second_operand = instruction.operands[1]

        if instruction.instruction in [Instruction.XORQ, Instruction.XORL] and \
                first_operand.type in [Operand.OperandType.REGISTER, Operand.OperandType.MEMORY] and \
                second_operand.type in [Operand.OperandType.REGISTER, Operand.OperandType.MEMORY]:

            sz = instruction.instruction[3]  # q or l

            random_register = Registers.get_random_register(instruction.get_bits())
            if random.randint(0, 1) % 2 == 0:
                """
                    c = random_register

                    a ^= c
                    b ^= c 
                    b ^= a
                """
                return [
                    f'\txor{sz} {random_register}, {first_operand.text}\n',
                    f'\txor{sz} {random_register}, {second_operand.text}\n',
                    f'\txor{sz} {first_operand.text}, {second_operand.text}\n',
                ]
            else:
                """
                    c = random_register

                    a ^= c
                    b ^= a 
                    b ^= c
                """
                return [
                    f'\txor{sz} {random_register}, {first_operand.text}\n',
                    f'\txor{sz} {first_operand.text}, {second_operand.text}\n',
                    f'\txor{sz} {random_register}, {second_operand.text}\n',
                ]

        else:
            return self.identity_morpher.morph_instruction(instruction)


class ValueBuilder:

    def build_immediate_value(self, immediate: int, bits: int) -> tuple[int, int]:
        self.check_immediate(immediate, bits)
        sign = 1 if immediate > 0 else -1
        abs = sign * immediate
        r = random.randint(0, abs)
        return sign * r, sign * (abs - r)

    def check_immediate(self, immediate: int, bits: int):
        limit = 1 << bits
        if not 0 < immediate + limit < 2 * limit:
            raise Exception('Cannot handle immediate {immediate} for {sz} bits')

    def negate_immediate(self, immediate: int, bits: int):
        self.check_immediate(immediate, bits)
        if immediate >= 0:
            return (1 << bits) - immediate
        else:
            return (1 << bits) + immediate


value_builder = ValueBuilder()
