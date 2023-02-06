"""
Create a ground truth file of listings and `owl:sameAs` links between
the listings
"""
import argparse
import csv
import itertools
import random
from typing import Iterator


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


def format_duplicates(duplicates: list[list[str]]) -> Iterator[list]:
    """
    Given a list of duplicates like the following:
        [
            [ A, B, C ],
            [ D, E ]
        ]

    Yield lists to express each duplication:
        ["+", A, B, 0]
        ["+", A, C, 0]
        ["+", B, C, 0]
        ["+", D, E, 0]

    Change this function and `format_non_duplicates` in order to
    change the format of the output labels file.
    """
    for dups in duplicates:
        for combination in itertools.combinations(dups, 2):
            yield ["+", combination[0], combination[1], 0]


def format_non_duplicates(
    duplicates: list[list[str]], uniques: list[str]
) -> Iterator[list]:
    """
    Given a list of duplicates like the following:
        [
            [ A, B, C ],
            [ D, E ]
        ]

    And a list of unique listings like the following:
        [ F, G ]

    Yield lists to express each duplication:
        ["-", A, F, 0]
        ["-", A, G, 0]
        ["-", A, D, 0]
        ["-", A, E, 0]
        ["-", B, F, 0]
        ["-", B, G, 0]
        ["-", B, D, 0]
        ["-", B, E, 0]
        ["-", C, F, 0]
        ["-", C, G, 0]
        ["-", C, D, 0]
        ["-", C, E, 0]
        ["-", D, F, 0]
        ["-", D, G, 0]
        ["-", E, F, 0]
        ["-", E, G, 0]
        ["-", F, G, 0]

    Change this function and `format_duplicates` in order to
    change the format of the output labels file.

    Call this function if you intend to represent each non-duplicated
    pair of items. Be aware that this will result in a large number of
    non-duplicated pairs, resulting in a gigantic output labels file.
    Instead, consider trying to represent only duplicated lines, and
    assume that all other lines are non-duplicated.
    """

    def _format_non_duplicates(first: str, second: str) -> list:
        return ["-", first, second, 0]

    # Duplicates are not equal to unique listings: A != B
    for dup in itertools.chain.from_iterable(duplicates):
        for unique in uniques:
            yield _format_non_duplicates(dup, unique)

    # Duplicates are not equal to different duplicates: A != D
    for dups in duplicates:
        for other_dup in (
            item
            for item in itertools.chain.from_iterable(duplicates)
            if item not in dups
        ):
            yield _format_non_duplicates(dups[0], other_dup)

    # Unique listings are not equal to each other: F != G
    for unique in itertools.combinations(uniques, 2):
        yield _format_non_duplicates(unique[0], unique[1])


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
        random.shuffle(labels)
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
