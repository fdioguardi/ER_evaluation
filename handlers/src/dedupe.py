import csv
import itertools
import os

import dedupe

from . import errors


class DedupeFormatter:
    def write_all(self, filename: str, duplicates, non_duplicates) -> None:

        if os.path.exists(filename):
            raise errors.FileExistsError(filename)

        data: dict = {
            "match": [({"uri": d1}, {"uri": d2}) for d1, d2 in duplicates],
            "distinct": [({"uri": n1}, {"uri": n2}) for n1, n2 in non_duplicates],
        }

        with open(filename, "w") as f:
            dedupe.write_training(data, f)

    def write_duplicates(self, filename: str, duplicates) -> None:
        self.write_all(filename, duplicates, non_duplicates=[])

    def read_duplicates(self, filename: str):
        if not os.path.exists(filename):
            raise errors.FileNotFoundError(filename)

        duplicates: dict[int, list[str]] = {}
        with open(filename, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                cluster = int(row["Cluster ID"])
                duplicates.get(cluster, []).append(row["uri"])

        for dups in duplicates.values():
            for combination in itertools.combinations(dups, 2):
                yield combination
