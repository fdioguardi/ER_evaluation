import csv
from collections.abc import Generator
from typing import Iterable


class JedaiHandler:
    """
    Handler for the JedAI duplicate detection tool input and output
    files.

    The default format is a CSV file in which each row represents a
    tuple of duplicate IDs.
    """

    def read_dups(self, filename: str) -> Generator[tuple[str, str], None, None]:
        """
        Read the duplicate IDs from the file.

        Args:
            filename (str): The path to the file.

        Yields:
            tuple[str, str]: The duplicate IDs.
        """
        with open(filename, "r") as f:
            reader = csv.reader(f)
            yield from ((row[0], row[1]) for row in reader)

    def read_non_dups(self, _: str) -> Generator[tuple[str, str], None, None]:
        """
        Read the non-duplicate IDs from the file.
        """
        yield from ()

    def write(
        self,
        filename: str,
        datafile: str,
        duplicates: Iterable[tuple[str, str]],
        non_dups: Iterable[tuple[str, str]],
    ):
        """
        Write the duplicate IDs to the file.

        Args:
            filename (str): The path to the file.
            datafile (str): The path to the data file.
            duplicates (list[tuple[str, str]]): The duplicate IDs.
            non_dups (list[tuple[str, str]]): The non-duplicate IDs.
        """
        with open(filename, "w") as f:
            writer = csv.writer(f)
            writer.writerows(duplicates)



    def extension(self) -> str:
        """
        Return the extension of the file format that the writer writes.

        Returns:
            The extension of the file format that the writer writes.
        """
        return ".jedai.csv"
