"""
The `duke` module provides functions to format duplicate and
non-duplicate records similarly to the deduplication engine Duke
(https://github.com/larsga/Duke).
"""


import itertools
from typing import Iterator


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
