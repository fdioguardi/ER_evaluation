import csv
import os
from collections.abc import Generator, Iterable

from .errors import FileNotFoundError


class DukeHandler:
    def read(self, filename: str) -> Generator[tuple[str, str], None, None]:
        """
        Read the duplicates from a file in Duke's expected format.

        Args:
            filename (str): The name of the file to read from.

        Yields:
            tuple[str, str]: A tuple of duplicate files.

        Raises:
            FileNotFoundError: If the file does not exist.
        """
        if not os.path.exists(filename):
            raise FileNotFoundError(filename=filename)

        with open(filename, "r") as f:
            reader = csv.reader(f)
            yield from ((row[1], row[2]) for row in reader if row[0] == "+")

    def write(self, filename: str, duplicates: Iterable[tuple[str, str]]) -> None:
        """
        Write the duplicates to a file in Duke's expected.

        Args:
            filename (str): The name of the file to write to.
            duplicates (Iterable[tuple[str, str]]): A list of tuples of
                duplicate files.

        Raises:
            FileExistsError: If the file already exists.
        """
        if os.path.exists(filename):
            raise FileExistsError(f"File `{filename}` already exists.")

        with open(filename, "w") as f:
            writer = csv.writer(f)
            for duplicate in duplicates:
                writer.writerow(["+", duplicate[0], duplicate[1], 0])
