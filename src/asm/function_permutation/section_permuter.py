import regex

from asm.utils import generate_permutation
from asm.morphing_pass import MorphingPass


class Section:

    def __init__(self, *,
                 line_number: int,
                 text: str,
                 sec_type: str,
                 name: str):
        self.start = line_number
        self.text = text
        self.sec_type = sec_type
        self.name = name
        self.end = line_number


class SectionPartition:

    def __init__(self,
                 first_section: int,
                 last_section: int,
                 sections_range: list[tuple[int, int]]) -> None:
        self.first_section = first_section
        self.last_section = last_section
        self.sections_start = sections_range


class SectionFinder:
    SECTION_START_PATTERN = r'\s*\.section\s+\.(\w+)\.(\w+)'

    def __init__(self, lines: list[str]):
        self.lines = lines

    def find_sections(self) -> SectionPartition:
        sections = []
        for ln, line in enumerate(self.lines):
            m = regex.match(SectionFinder.SECTION_START_PATTERN, line)
            if m is not None and m.group(1) == 'text':
                section = Section(
                    line_number=ln,
                    text=m.group(0),
                    sec_type=m.group(1),
                    name=m.group(2),
                )
                sections.append(section)

        if len(sections) == 0:
            return SectionPartition(
                0, 0, []
            )

        for i in range(0, len(sections) - 1):
            sections[i].end = sections[i + 1].start

        ranges = []
        i = 0
        while i < len(sections) - 1:
            start = sections[i].start
            j = i
            while j + 1 < len(sections) and sections[j + 1].name == sections[i].name:
                j += 1
            end = sections[j].end
            i = j + 1
            ranges.append((start, end))

        return SectionPartition(
            sections[0].start,
            sections[-1].start,
            ranges
        )


class SectionPermutationPass(MorphingPass):

    def morph_lines(self) -> list[str]:
        section_finder = SectionFinder(self.lines)
        partition = section_finder.find_sections()
        n = len(partition.sections_start)
        print(partition.sections_start)
        # breakpoint()
        permutation = generate_permutation(n)
        new_lines = []
        new_lines.extend(self.lines[:partition.first_section])
        for ind in permutation:
            rs, re = partition.sections_start[ind]
            new_lines.extend(self.lines[rs:re])
        new_lines.extend(self.lines[partition.last_section:])
        return new_lines
