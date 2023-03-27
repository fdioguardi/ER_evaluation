from typing import Protocol


class Reader(Protocol):
    def read_duplicates(self, filename: str):
        """
        Read in a file and return a tuple containing a list of duplicate
        pairs and a list of non-duplicate pairs.

        Args:
            filename: The name of the file to read from.

        Returns:
            A tuple containing a list of duplicate pairs and a list of
            non-duplicate pairs.

        Errors:
            FileNotFoundError: If the file does not exist.
            ValueError: If the file is not in the correct format.
        """
        ...

    def read_all(self, filename: str):
        """
        Read in a file and return a list of all the lines.

        Args:
            filename: The name of the file to read from.

        Returns:
            A list of all the lines in the file.

        Errors:
            FileNotFoundError: If the file does not exist.
        """
        ...


class Writer(Protocol):
    def write_duplicates(self, filename: str, duplicates) -> None:
        """
        Write duplicates to a file in the format specified by the
        writer.

        Args:
            filename: The name of the file to write to.
            duplicates: A list of tuples representing the duplicate
            pairs.

        Errors:
            FileExistsError: If the file already exists.
        """
        ...

    def write_all(self, filename: str, duplicates, non_duplicates) -> None:
        """
        Write both duplicates and non-duplicates to a file in the format
        specified by the writer.

        Args:
            filename: The name of the file to write to.
            duplicates: A list of tuples representing the duplicate
                pairs.
            non_duplicates: A list of tuples representing the
                non-duplicate pairs.

        Errors:
            FileExistsError: If the file already exists.
        """
        ...
