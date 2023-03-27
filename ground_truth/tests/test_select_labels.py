import unittest
from unittest.mock import patch

from src.gt import select_labels


class TestSelectLabels(unittest.TestCase):
    """
    Test suite for the select_labels function in generate_gt.py
    """

    def setUp(self) -> None:
        """
        Set up the test case by initializing the labels list
        """
        self.labels = [
            ["A", "B", "C"],
            ["D", "E"],
            ["F", "G", "H", "I"],
            ["J", "K", "L"],
            ["M", "N"],
        ]

    def test_select_labels_deterministic(self):
        """
        Test the select_labels function with deterministic behavior
        """
        expected_duplicates = [["A", "B", "C"], ["D", "E"]]
        expected_uniques = ["F", "J", "M"]

        self.assertEqual(
            select_labels(self.labels, False), (expected_duplicates, expected_uniques)
        )

    def test_select_labels_random(self):
        """
        Test the select_labels function with random behavior
        """
        expected_duplicates = [["A", "B", "C"], ["F", "G", "H", "I"]]
        expected_uniques = ["E", "L", "N"]

        with patch(
            "random.sample",
            return_value=[
                ["A", "B", "C"],
                ["F", "G", "H", "I"],
                ["D", "E"],
                ["J", "K", "L"],
                ["M", "N"],
            ],
        ):
            with patch("random.choice", lambda values: values[-1]):
                duplicates, uniques = select_labels(self.labels, True)
                self.assertListEqual(sorted(duplicates), sorted(expected_duplicates))
                self.assertListEqual(sorted(uniques), sorted(expected_uniques))


if __name__ == "__main__":
    unittest.main()
