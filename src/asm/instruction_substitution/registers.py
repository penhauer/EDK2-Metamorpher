import random


class Registers:
    TABLE = """
    64              | 32            | 16            | 8 
    rax             | eax           | ax            | al
    rbx             | ebx           | bx            | bl
    rcx             | ecx           | cx            | cl
    rdx             | edx           | dx            | dl
    rsi             | esi           | si            | sil
    rdi             | edi           | di            | dil
    rbp             | ebp           | bp            | bpl
    rsp             | esp           | sp            | spl
    r8              | r8d           | r8w           | r8b
    r9              | r9d           | r9w           | r9b
    r10             | r10d          | r10w          | r10b
    r11             | r11d          | r11w          | r11b
    r12             | r12d          | r12w          | r12b
    r13             | r13d          | r13w          | r13b
    r14             | r14d          | r14w          | r14b
    r15             | r15d          | r15w          | r15b
    """

    @staticmethod
    def _parse_table(table: str):
        lines = table.split('\n')
        lines = list(filter(lambda line: line.strip() != "", lines))

        def parse_line(line: str) -> list[str]:
            return list(map(lambda x: x.strip(), line.split('|')))

        sizes = parse_line(lines[0])
        registers = list(map(parse_line, lines[1:]))
        return sizes, registers

    SIZES, REGISTERS = _parse_table(TABLE)

    @classmethod
    def get_random_register(cls, size: int):
        column = cls.SIZES.index(str(size))
        row = random.randint(0, len(cls.REGISTERS) - 1)
        return f'%{cls.REGISTERS[row][column]}'
