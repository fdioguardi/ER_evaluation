"""
Create a ground truth file of listings and `owl:sameAs` links between
the listings
"""
import argparse
import csv
import itertools
import random
from typing import Iterator

from ...format.default import format_duplicates, format_non_duplicates


def main() -> None:
    """
    Take a CSV dataset of real estate listings and a CSV of known
    owl:sameAs links between them.

    Generate a new CSV dataset of some duplicated real estate listings
    and some unique ones. Output a CSV of owl:sameAs links between the
    duplicated listings.

    Effectively, remove some listings from both input files to
    ensure the output contains both duplicated and unique listings.

    Example:
        If the input dataset contains information about listings A, B,
        C, D, E, F, G, and H.
        And the input labels contains the following links:
            A <-> B
            C <-> D
            E <-> F
            G <-> H

        Generate an output dataset containing information about listings
        A, B, C, D, E, and G.
        And an output file of labels containing the following links:
            A <-> B
            C <-> D

        Meaning E and G will be unique listings in the output dataset.
    """
    args: argparse.Namespace = read_args()

    # Generate output labels file based on input labels file
    with open(args.input_labels, "r") as input_labels:
        with open(args.output_labels, "w") as output_labels:
            labels = csv.reader(input_labels)
            labels = [duplicates[0].split(";") for duplicates in labels]

            duplicates, uniques = select_labels(labels, args.randomize)

            writer = csv.writer(output_labels)
            writer.writerows(format_duplicates(duplicates))
            writer.writerows(format_non_duplicates(duplicates, uniques))

            del labels

    # Generate output data file from selected listing IDs
    uris: set = set(itertools.chain.from_iterable(duplicates)) | set(uniques)
    del uniques, duplicates

    with open(args.input_data, "r") as input_data:
        with open(args.output_data, "w") as output_data:
            reader = csv.DictReader(input_data)
            assert reader.fieldnames

            writer = csv.DictWriter(output_data, fieldnames=sorted(reader.fieldnames))
            writer.writeheader()

            writer.writerows(row for row in reader if row["uri"] in uris)


def select_labels(
    labels: list[list[str]], randomize: bool
) -> tuple[list[list[str]], list[str]]:
    """
    Given a list of duplicates that contains the following links:
        A <-> B <-> X
        C <-> D
        E <-> F
        G <-> H

    Remove some of the duplicates to ensure the output
    contains both duplicated and unique listings.

    If `randomize` is True, the label selection will be randomized.
    Otherwise, the first half of the labels will be selected.

    Return a list of links that contains (e.g.) the following links:
        A <-> B <-> X
        E <-> F
    """
    if randomize:
        labels = random.sample(labels, k=len(labels))
        uniques: list[str] = [
            random.choice(dups) for dups in labels[len(labels) // 2 :]
        ]
    else:
        uniques: list[str] = [dups[0] for dups in labels[len(labels) // 2 :]]

    return labels[: len(labels) // 2], uniques


def read_args() -> argparse.Namespace:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        "-r",
        "--randomize",
        action="store_false",
        help="randomize the data selection",
    )

    parser.add_argument(
        "--input-labels",
        default="input/labels.csv",
        help="input labels file",
        type=str,
    )
    parser.add_argument(
        "--input-data",
        default="input/data.csv",
        help="input CSV file containing labeled data",
        type=str,
    )

    parser.add_argument(
        "--output-labels",
        default="output/labels.csv",
        help="output file of owl:sameAs-equivalent links",
        type=str,
    )
    parser.add_argument(
        "--output-data",
        default="output/data.csv",
        help="destination file for the generated dataset",
        type=str,
    )

    return parser.parse_args()


if __name__ == "__main__":
    main()
