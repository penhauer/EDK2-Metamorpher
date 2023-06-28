import enum

import regex


class Operand:
    class OperandType(enum.Enum):
        REGISTER = 1,
        MEMORY = 2,
        IMMEDIATE_VALUE = 3,

    def __init__(self, op_type: OperandType, **kwargs) -> None:
        self.type = op_type
        self.text = kwargs.get('text')
        self.register: str = kwargs.get('register', None)
        self.immediate: str = kwargs.get('immediate', None)
        self.offset: str = kwargs.get('offset', None)


class Instruction:
    SIZE_8_BITS = 8
    SIZE_16_BITS = 16
    SIZE_32_BITS = 32
    SIZE_64_BITS = 64

    MOVB = 'movb'
    MOVL = 'movl'
    MOVQ = 'movq'
    MOVZBL = 'movzbl'

    XORQ = 'xorq'
    XORL = 'xorl'

    ANDB = 'andb'
    ANDL = 'andl'
    ANDQ = 'andq'

    def __init__(self, text: str, instruction: str, operands: list[Operand]) -> None:
        self.text = text
        self.instruction = instruction
        self.operands = operands

    def get_bits(self):
        if self.instruction == Instruction.XORQ:
            return Instruction.SIZE_64_BITS
        elif self.instruction == Instruction.XORL:
            return Instruction.SIZE_32_BITS
        elif self.instruction == Instruction.ANDQ:
            return Instruction.SIZE_64_BITS
        elif self.instruction == Instruction.ANDL:
            return Instruction.SIZE_32_BITS
        if self.instruction == Instruction.ANDB:
            return Instruction.SIZE_8_BITS
        if self.instruction == Instruction.MOVQ:
            return Instruction.SIZE_64_BITS
        if self.instruction == Instruction.MOVL:
            return Instruction.SIZE_32_BITS
        if self.instruction == Instruction.MOVB:
            return Instruction.SIZE_8_BITS
        else:
            raise NotImplementedError(f'get_bits for instrution {self.instruction} is not defined')

    def __str__(self) -> str:
        return self.text


class InstructionFactory:
    LABEL_PATTERN = r'\.L\d+:'
    # TWO_OPERAND_INSTRUCTIONS = r'(?P<instruction>movl|movq|movw|movzbl|xorl|addq|subq)'
    TWO_OPERAND_INSTRUCTIONS = r'(?P<instruction>\w{2,5})'
    REGISTER_PATTERN = fr'(?P<register>%\w{{2,3}})'
    IMMEDIATE_VALUE_PATTERN = fr'(?:\$(?P<immediate>-?\d+))'
    MEMORY_LOCATION_PATTERN = fr'((?P<offset>\d+)\({REGISTER_PATTERN}\))'
    OPERAND_PATTERN = fr'({REGISTER_PATTERN}|{IMMEDIATE_VALUE_PATTERN}|{MEMORY_LOCATION_PATTERN})'
    TWO_OPERAND_PATTERN = fr'^\s*{TWO_OPERAND_INSTRUCTIONS}\s+{OPERAND_PATTERN},\s+{OPERAND_PATTERN}\s*$'

    def __init__(self) -> None:
        pass

    @staticmethod
    def perform_tests():
        assert regex.match(InstructionFactory.TWO_OPERAND_INSTRUCTIONS, 'movl')
        assert regex.match(InstructionFactory.REGISTER_PATTERN, '%rax')
        assert regex.match(InstructionFactory.IMMEDIATE_VALUE_PATTERN, '$80')
        assert regex.match(InstructionFactory.OPERAND_PATTERN, '%rax')

    def get_instruction(self, line: str) -> Instruction | None:
        # InstructionFactory.perform_tests()

        if m := regex.match(InstructionFactory.TWO_OPERAND_PATTERN, line):
            return self._parse_two_operands(m)

        return None

    def _parse_two_operands(self, m: regex.Match) -> Instruction:
        instruction = m.group(1)
        first_operand = self._parse_operand(m.group(2))
        second_operand = self._parse_operand(m.group(7))
        return Instruction(
            m.group(0),
            instruction,
            [first_operand, second_operand],
        )

    def _parse_operand(self, operand: str):
        m = regex.match(InstructionFactory.OPERAND_PATTERN, operand)
        d = m.groupdict()

        if d.get('memory', None):
            operand_type = Operand.OperandType.MEMORY
        elif d.get('immediate', None):
            operand_type = Operand.OperandType.IMMEDIATE_VALUE
        elif d.get('register', None):
            operand_type = Operand.OperandType.REGISTER
        else:
            raise NotImplementedError(f'not supported operand for `{operand}`')

        return Operand(
            op_type=operand_type,
            text=m.group(0),
            **d,
        )
