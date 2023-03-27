import os
import csv
from .errors import FileNotFoundError


class DukeFormatter:
    def read_duplicates(self, filename: str):
        if not os.path.exists(filename):
            raise FileNotFoundError(filename=filename)

        with open(filename, "r") as f:
            reader = csv.reader(f)
            return [(row[1], row[2]) for row in reader if row[0] == "+"]

    def read_all(self, filename: str):
        if not os.path.exists(filename):
            raise FileNotFoundError(filename=filename)

        duplicates: list[tuple[str, str]] = []
        non_duplicates: list[tuple[str, str]] = []
        with open(filename, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                if row[0] == "+":
                    duplicates.append((row[1], row[2]))
                elif row[0] == "-":
                    non_duplicates.append((row[1], row[2]))
                else:
                    raise ValueError(f"Invalid row: {row}")

        return duplicates, non_duplicates

    def write_duplicates(self, filename: str, duplicates) -> None:
        if os.path.exists(filename):
            raise FileExistsError(f"File `{filename}` already exists.")

        with open(filename, "w") as f:
            writer = csv.writer(f)
            for duplicate in duplicates:
                writer.writerow(["+", duplicate[0], duplicate[1], 0])

    def write_all(self, filename: str, duplicates, non_duplicates) -> None:

        self.write_duplicates(filename, duplicates)

        with open(filename, "a") as f:
            writer = csv.writer(f)
            for non_duplicate in non_duplicates:
                writer.writerow(["-", non_duplicate[0], non_duplicate[1], 0])
