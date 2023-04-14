from typing import Generator, Iterable, Protocol


class Reader(Protocol):
    def read(self, filename: str) -> Generator[tuple[str, str], None, None]:
        """
        Read in a file and return a tuple containing a list of duplicate
        pairs and a list of non-duplicate pairs.

        Args:
            filename: The name of the file to read from.

        Yields:
            A tuple containing a pair of duplicates.

        Errors:
            FileNotFoundError: If the file does not exist.
            ValueError: If the file is not in the correct format.
        """
        ...


class Writer(Protocol):
    def write(self, filename: str, duplicates: Iterable[tuple[str, str]]) -> None:
        """
        Write duplicates to a file in the format specified by the
        writer.

        Args:
            filename: The name of the file to write to.
            duplicates: An iterable of tuples representing the duplicate
            pairs.

        Errors:
            FileExistsError: If the file already exists.
        """
        ...
