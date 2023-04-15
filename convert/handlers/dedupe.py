import csv
import itertools
import os
from collections.abc import Generator, Iterable

import dedupe

from . import errors


class DedupeHandler:
    """
    A class to handle the formatting of data for dedupe.

    It implements the protocol for reading and writing the training data
    for dedupe.
    """

    def read(self, filename: str) -> Generator[tuple[str, str], None, None]:
        """
        Read the duplicates from a file in dedupe's expected format.

        Args:
            filename (str): The name of the file to read from.

        Yields:
            tuple[str, str]: A tuple of duplicate files.

        Raises:
            FileNotFoundError: If the file does not exist.
        """
        if not os.path.exists(filename):
            raise errors.FileNotFoundError(filename)

        duplicates: dict[int, list[str]] = {}
        with open(filename, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                cluster = int(row["Cluster ID"])
                duplicates.get(cluster, []).append(row["uri"])

        for dups in duplicates.values():
            if len(dups) < 2:
                continue

            for combination in itertools.combinations(dups, 2):
                yield combination

    def write(self, filename: str, duplicates: Iterable[tuple[str, str]]) -> None:
        """
        Write the duplicates to a file in dedupe's expected.

        Args:
            filename (str): The name of the file to write to.
            duplicates (Iterable[tuple[str, str]]): A list of tuples of
                duplicate files.

        Raises:
            FileExistsError: If the file already exists.
            FileNotFoundError: If the data file does not exist.
        """

        if os.path.exists(filename):
            raise errors.FileExistsError(filename)

        dirname = os.path.dirname(__file__)
        data_file = os.path.join(dirname, "../input/data.csv")

        if not os.path.exists(data_file):
            raise errors.FileNotFoundError(data_file)

        with open(data_file, "r") as f:
            reader = csv.DictReader(f)
            # each row has an uri and a lot of fields
            # create a data_attrs as dict. its key will be the uri and the value everything

            data_attrs = {row["uri"]: self.normalize(row) for row in reader}

        data: dict = {
            "match": [(data_attrs[d1], data_attrs[d2]) for d1, d2 in duplicates],
            "distinct": [],
        }

        with open(filename, "w") as f:
            dedupe.write_training(data, f)

    def normalize(self, row: dict) -> dict:
        """
        Normalize the data for dedupe.

        Args:
            row (dict): A record of the data.

        Returns:
            dict: The normalized data.
        """
        if row.get("coordinates"):
            row["coordinates"] = f"({row['coordinates']})"

        return row
