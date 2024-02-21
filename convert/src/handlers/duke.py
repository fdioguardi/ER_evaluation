import csv
from collections.abc import Generator, Iterable


class DukeHandler:
    def read_dups(self, filename: str) -> Generator[tuple[str, str], None, None]:
        """
        Read the duplicates from a file in Duke's expected format.

        Args:
            filename (str): The name of the file to read from.

        Yields:
            tuple[str, str]: A tuple of duplicate files.
        """
        with open(filename, "r") as f:
            reader = csv.reader(f)
            yield from ((row[1], row[2]) for row in reader if row[0] == "+")

    def read_non_dups(self, filename: str) -> Generator[tuple[str, str], None, None]:
        """
        Read the non-duplicates from a file in Duke's expected format.

        Args:
            filename (str): The name of the file to read from.

        Yields:
            tuple[str, str]: A tuple of non-duplicate files.
        """
        with open(filename, "r") as f:
            reader = csv.reader(f)
            yield from ((row[1], row[2]) for row in reader if row[0] == "-")

    def write(
        self,
        filename: str,
        _: str,
        duplicates: Iterable[tuple[str, str]],
        non_dups: Iterable[tuple[str, str]],
    ) -> None:
        """
        Write the (non-)duplicates to a file in Duke's expected.

        Args:
            filename (str): The name of the file to write to.
            datafile (str): The name of the datafile.
            duplicates (Iterable[tuple[str, str]]): A list of tuples of
                duplicate pairs.
            non_dups (Iterable[tuple[str, str]]): A list of tuples of
                non-duplicate pairs.
        """
        with open(filename, "w") as f:
            writer = csv.writer(f)
            for duplicate in duplicates:
                writer.writerow(["+", duplicate[0], duplicate[1], 0])
            for non_dup in non_dups:
                writer.writerow(["-", non_dup[0], non_dup[1], 0])

    @property
    def extension(self) -> str:
        """
        Return the extension of the file format that the writer writes.

        Returns:
            The extension of the file format that the writer writes.
        """
        return ".duke.csv"
