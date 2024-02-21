import csv
import itertools
import math
import re
from collections.abc import Generator, Iterable
from typing import Any

import dedupe
from dedupe._typing import RecordDict, TrainingData
from unidecode import unidecode


class DedupeHandler:
    """
    A class to handle the formatting of data for dedupe.

    It implements the protocol for reading and writing the training data
    for dedupe.
    """

    def read_dups(self, filename: str) -> Generator[tuple[str, str], None, None]:
        """
        Read the duplicates from a file in dedupe's expected format.

        Args:
            filename (str): The name of the file to read from.

        Yields:
            tuple[str, str]: A tuple of duplicate files.
        """
        duplicates: dict[int, list[str]] = {}
        with open(filename, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                cluster = int(row["Cluster ID"])
                duplicates[cluster] = duplicates.get(cluster, []) + [row["uri"]]

        for dups in duplicates.values():
            if len(dups) < 2:
                continue

            for combination in itertools.combinations(dups, 2):
                yield combination

    def read_non_dups(self, filename: str) -> Generator[tuple[str, str], None, None]:
        """
        Read the non duplicates from a file in dedupe's expected format.

        Args:
            filename (str): The name of the file to read from.

        Yields:
            tuple[str, str]: A tuple of non duplicate files.
        """
        duplicates: dict[int, list[str]] = {}
        with open(filename, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                cluster = int(row["Cluster ID"])
                duplicates[cluster] = duplicates.get(cluster, []) + [row["uri"]]

        for dups in duplicates.values():
            if len(dups) > 1:
                continue

            for combination in itertools.combinations(dups, 2):
                yield combination

    def write(
        self,
        filename: str,
        datafile: str,
        duplicates: Iterable[tuple[str, str]],
        non_dups: Iterable[tuple[str, str]],
    ) -> None:
        """
        Write the duplicates to a file in dedupe's expected.

        Args:
            filename (str): The name of the file to write to.
            datafile (str): The name of the file with the information of
                each item.
            duplicates (Iterable[tuple[str, str]]): A list of tuples of
                duplicate files.

        """
        with open(datafile, "r") as f:
            reader = csv.DictReader(f)
            data_attrs: dict[str, RecordDict] = {
                row["uri"]: self.normalize(row) for row in reader
            }

        training_data: TrainingData = {
            "match": [(data_attrs[d1], data_attrs[d2]) for d1, d2 in duplicates],
            "distinct": [(data_attrs[d1], data_attrs[d2]) for d1, d2 in non_dups],
        }

        with open(filename, "w") as f:
            dedupe.write_training(training_data, f)

    def normalize(self, row: dict[str, Any]) -> dict[str, Any]:
        """
        Normalize the data for dedupe.

        Args:
            row (dict[str, Any]): The row to normalize.

        Returns:
            dict[str, Any]: The normalized row.
        """
        for k, v in row.items():
            v = unidecode(v)
            v = re.sub("  +", " ", v)
            v = re.sub("\n", " ", v)
            v = v.strip().strip('"').strip("'").lower().strip()
            row[k] = v

            if not v:
                row[k] = None
                continue

            if k in ("age", "bath_amnt", "room_amnt", "garage_amnt", "bed_amnt"):
                if math.floor(float(v)) == float(v):
                    row[k] = int(math.floor(float(v)))
            elif k in (
                "total_surface",
                "covered_surface",
                "land_surface",
                "maintenance_fee",
                "price",
            ):
                row[k] = "null" if float(v) == float("NaN") else float(v)
            elif k == "coordinates":
                row[k] = tuple(map(float, v.strip("()").split(",")))

        return row

    @property
    def extension(self) -> str:
        """
        Return the extension of the file format that the writer writes.

        Returns:
            The extension of the file format that the writer writes.
        """
        return ".dedupe.json"
