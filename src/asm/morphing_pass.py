import abc


class MorphingPass(abc.ABC):

    def __init__(self, lines: list[str]):
        self.lines = lines

    @abc.abstractmethod
    def morph_lines(self) -> list[str]:
        pass