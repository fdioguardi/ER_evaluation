from typing import Generator, Iterable, Protocol


class Reader(Protocol):
    def read_dups(self, filename: str) -> Generator[tuple[str, str], None, None]:
        """
        Read in a file and return a tuple containing a list of
        duplicate pairs and a list of non-duplicate pairs.

        Args:
            filename: The name of the file to read from.

        Yields:
            A tuple containing a pair of duplicates.
        """
        ...

    def read_non_dups(self, filename: str) -> Generator[tuple[str, str], None, None]:
        """
        Read in a file and return a tuple containing a list of
        non-duplicate pairs and a list of non-duplicate pairs.

        Args:
            filename: The name of the file to read from.

        Yields:
            A tuple containing a pair of duplicates.
        """
        ...


class Writer(Protocol):
    def write(
        self,
        filename: str,
        datafile: str,
        duplicates: Iterable[tuple[str, str]],
        non_dups: Iterable[tuple[str, str]],
    ) -> None:
        """
        Write (non-)duplicates to a file in the format specified by the
        writer.

        Args:
            filename: The name of the file to write to.
            datafile: The name of the file with the data of each record.
            duplicates: An iterable of tuples representing the duplicate
                pairs.
            non_dups: An iterable of tuples representing the
                non-duplicate pairs.
        """
        ...

    def extension(self) -> str:
        """
        Return the extension of the file format that the writer writes.

        Returns:
            The extension of the file format that the writer writes.
        """
        ...


class Handler(Reader, Writer, Protocol):
    """
    A protocol for a handler that can read and write duplicate pairs.
    """

    ...
