import argparse
import os
import unittest
from io import StringIO
from unittest.mock import patch

from metrics.metrics import (
    ConfusionMatrix,
    Metrics,
    calculate_confusion_matrix,
    calculate_metrics,
    main,
    read_pairs_from_file,
)


class TestDuplicateDetectionMetrics(unittest.TestCase):
    """Test the duplicate detection metrics script."""

    def setUp(self):
        """Create two files with pairs of identifiers."""
        self.true_positives_file = "data/test_true_positives.csv"
        self.algorithm_positives_file = "data/test_algorithm_positives.csv"

        with open(self.true_positives_file, "w") as f:
            f.write("1,2\n2,3\n4,5\n")

        with open(self.algorithm_positives_file, "w") as f:
            f.write("1,2\n4,5\n6,7\n")

    def tearDown(self):
        """Remove the files created in the setup."""
        os.remove(self.true_positives_file)
        os.remove(self.algorithm_positives_file)

    def test_read_pairs_from_file(self):
        """Test that the pairs are read correctly from the file."""
        expected_pairs = {
            frozenset(["1", "2"]),
            frozenset(["2", "3"]),
            frozenset(["4", "5"]),
        }
        pairs = read_pairs_from_file(self.true_positives_file)
        self.assertEqual(
            pairs, expected_pairs, msg="Pairs read from file are incorrect"
        )

    def test_calculate_confusion_matrix(self):
        """Test that the confusion matrix is calculated correctly."""
        true_positives = {frozenset(["1", "2"]), frozenset(["4", "5"])}
        algorithm_positives = {frozenset(["1", "2"]), frozenset(["6", "7"])}
        expected_cm = ConfusionMatrix(tp=1, fp=1, fn=1)

        cm = calculate_confusion_matrix(true_positives, algorithm_positives)
        self.assertEqual(cm, expected_cm)

    def test_calculate_metrics(self):
        """Test that the metrics are calculated correctly."""
        cm = ConfusionMatrix(tp=1, fp=1, fn=1)
        expected_metrics = Metrics(precision=0.5, recall=0.5, f1_score=0.5)

        metrics = calculate_metrics(cm)
        self.assertEqual(metrics, expected_metrics)

    @patch("argparse.ArgumentParser.parse_args")
    @patch("sys.stdout", new_callable=StringIO)
    def test_main(self, mock_stdout, mock_parse_args):
        """Test that the main function prints the correct output."""
        expected_output = (
            "Correct links found: 2 / 3\n"
            "Precision: 0.667\n"
            "Recall: 0.667\n"
            "F1-score: 0.667\n"
        )

        mock_parse_args.return_value = argparse.Namespace(
            true_positives_file=self.true_positives_file,
            algorithm_positives_file=self.algorithm_positives_file,
        )

        main()

        self.assertEqual(mock_stdout.getvalue(), expected_output)


if __name__ == "__main__":
    unittest.main()
