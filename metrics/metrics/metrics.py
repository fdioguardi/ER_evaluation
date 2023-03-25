"""
Module to measure the precision, recall, and F1-score of a duplicate
detection algorithm.

Input file format:
The input files should contain one match per line, in the following format:
ID1,ID2
ID2,ID3
ID4,ID5
...
"""


import argparse
import collections
import csv
import os

ConfusionMatrix = collections.namedtuple("ConfusionMatrix", ["tp", "fp", "fn"])
Metrics = collections.namedtuple("Metrics", ["precision", "recall", "f1_score"])


def read_pairs_from_file(file_path: str) -> set[frozenset[str]]:
    """
    Reads a CSV file containing pairs of IDs and returns a set of
    frozensets.

    Parameters:
    file_path (str): Path to a CSV file containing pairs of IDs.

    Returns:
    A set of frozensets, each containing two IDs.
    """
    with open(file_path, "r") as f:
        reader = csv.reader(f)
        return {frozenset(row) for row in reader}


def calculate_confusion_matrix(true_pos: set, algorithm_pos: set) -> ConfusionMatrix:
    """
    Calculate the confusion matrix given true and algorithm positives.

    Args:
        true_pos (set): a set with the true positive matches.
        algorithm_pos (set): a set with the algorithm positive matches.

    Returns:
        ConfusionMatrix: the confusion matrix as a namedtuple with tp,
        fp, fn.
    """
    return ConfusionMatrix(
        tp=len(true_pos & algorithm_pos),
        fp=len(algorithm_pos - true_pos),
        fn=len(true_pos - algorithm_pos),
    )


def calculate_metrics(cm: ConfusionMatrix) -> Metrics:
    """
    Calculate precision, recall and F1-score given the confusion
    matrix.

    Args:
        cm (ConfusionMatrix): the confusion matrix as a namedtuple with
            tp, fp, fn.

    Returns:
        Metrics: the metrics as a namedtuple with precision, recall, f1_score.
    """

    precision = cm.tp / (cm.tp + cm.fp) if cm.tp + cm.fp > 0 else 0.0
    recall = cm.tp / (cm.tp + cm.fn) if cm.tp + cm.fn > 0 else 0.0
    f1_score = (
        2 * (precision * recall) / (precision + recall)
        if precision + recall > 0
        else 0.0
    )

    return Metrics(precision=precision, recall=recall, f1_score=f1_score)


def parse_args() -> argparse.Namespace:
    """
    Parse command line arguments.

    Returns:
        argparse.Namespace: the parsed arguments as an object.
    """
    parser = argparse.ArgumentParser(
        description="Calculates precision, recall and f1-score given true and algorithm positives"
    )
    parser.add_argument(
        "true_positives_file",
        type=str,
        help="path to the file with the true positive matches",
    )
    parser.add_argument(
        "algorithm_positives_file",
        type=str,
        help="path to the file with the algorithm positive matches",
    )

    args: argparse.Namespace = parser.parse_args()

    for file_path in [args.true_positives_file, args.algorithm_positives_file]:
        if not os.path.exists(file_path):
            raise argparse.ArgumentTypeError(f"File {file_path} does not exist")

    return args


def main() -> None:
    args: argparse.Namespace = parse_args()

    true_positives = read_pairs_from_file(args.true_positives_file)
    algorithm_positives = read_pairs_from_file(args.algorithm_positives_file)

    cm = calculate_confusion_matrix(true_positives, algorithm_positives)
    metrics = calculate_metrics(cm)

    print(f"Correct links found: {cm.tp} / {cm.tp + cm.fn}")
    print(f"Precision: {metrics.precision:.3f}")
    print(f"Recall: {metrics.recall:.3f}")
    print(f"F1-score: {metrics.f1_score:.3f}")


if __name__ == "__main__":
    main()
