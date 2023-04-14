import csv
import os
from collections.abc import Generator
from typing import Iterable

from .errors import FileExistsError, FileNotFoundError


class JedaiHandler:
    """
    Handler for the JedAI duplicate detection tool input and output
    files.

    The default format is a CSV file in which each row represents a
    tuple of duplicate IDs.
    """

    def read(self, filename: str) -> Generator[tuple[str, str], None, None]:
        """
        Read the duplicate IDs from the file.

        Args:
            filename (str): The path to the file.

        Yields:
            tuple[str, str]: The duplicate IDs.

        Raises:
            FileNotFoundError: If the file does not exist.
        """
        if not os.path.exists(filename):
            raise FileNotFoundError(filename)

        with open(filename, "r") as f:
            reader = csv.reader(f)
            yield from ((row[0], row[1]) for row in reader)

    def write(self, filename: str, duplicates: Iterable[tuple[str, str]]):
        """
        Write the duplicate IDs to the file.

        Args:
            filename (str): The path to the file.
            duplicates (list[tuple[str, str]]): The duplicate IDs.

        Raises:
            FileExistsError: If the file already exists.
        """
        if os.path.exists(filename):
            raise FileExistsError(filename)

        with open(filename, "w") as f:
            writer = csv.writer(f)
            writer.writerows(duplicates)
