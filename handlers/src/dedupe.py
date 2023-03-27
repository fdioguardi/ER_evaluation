import csv
import os

import networkx as nx
import dedupe

from . import errors

class DedupeFormatter:

    def write_all(self, filename: str, duplicates, non_duplicates) -> None:

        if os.path.exists(filename):
            raise errors.FileExistsError(filename)

        data: dict = {
                "match": [({'uri': d1}, {'uri': d2}) for d1, d2 in duplicates],
                "distinct": [({'uri': n1}, {'uri': n2}) for n1, n2 in non_duplicates]
        }   

        with open(filename, "w") as f:
            dedupe.write_training(f, data)

    def write_duplicates(self, filename: str, duplicates) -> None:
        self.write_all(filename, duplicates, non_duplicates=[])

    def read_duplicates(self, filename: str) -> list:
        if not os.path.exists(filename):
            raise errors.FileNotFoundError(filename)

        duplicates = nx.Graph()
        with open(filename, "r") as f:
            csv.DictReader(f)

            # file has Cluster Id, and uri. Return pairs of duplicates
