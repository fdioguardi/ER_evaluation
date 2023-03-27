import os
from .errors import FileNotFoundError
import csv


class DefaultFormatter:
    """ """

    def read_duplicates(self, filename: str):
        if not os.path.exists(filename):
            raise FileNotFoundError(filename)

        with open(filename, "r") as f:
            reader = csv.reader(f)
            yield from ((row[0], row[1]) for row in reader)

    def read_all(self, filename: str):
        yield from self.read_duplicates(filename)

    def write_duplicates(self, filename: str, duplicates: list[tuple[str, str]]):
        with open(filename, "w") as f:
            writer = csv.writer(f)
            writer.writerows(duplicates)

    def write_all(self, filename: str, duplicates: list[tuple[str, str]]):
        self.write_duplicates(filename, duplicates)
