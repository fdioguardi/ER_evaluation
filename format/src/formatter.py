from enum import Enum
from typing import Iterator, Protocol


class Mode(Enum):
    DUPLICATES_ONLY = 1
    DUPLICATES_AND_NON_DUPLICATES = 2


class Formatter(Protocol):
    def format(self, mode: Mode) -> Iterator[list]:
        ...
