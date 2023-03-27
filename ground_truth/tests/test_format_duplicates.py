import unittest

from src.gt import format_duplicates


class TestFormatDuplicates(unittest.TestCase):
    """
    Test suite for the `format_duplicates` function in the `generate_gt`
    module.

    The `format_duplicates` function takes a list of groups of duplicate
    labels and generates a list of tuples representing the relationships
    between the duplicate labels. This test suite tests various
    scenarios for the `format_duplicates` function.
    """

    def test_format_one_group_of_duplicates(self):
        """
        Test that `format_duplicates` correctly formats a list of one
        group of duplicate labels.

        The test case checks that `format_duplicates` generates a list
        of tuples representing the relationships between the duplicate
        labels.
        """
        duplicates = [["A", "B", "C"]]
        expected_output = [
            ["+", "A", "B", 0],
            ["+", "A", "C", 0],
            ["+", "B", "C", 0],
        ]
        self.assertEqual(list(format_duplicates(duplicates)), expected_output)

    def test_format_multiple_groups_of_duplicates(self):
        """
        Test that `format_duplicates` correctly formats a list of
        multiple groups of duplicate labels.

        The test case checks that `format_duplicates` generates a list
        of tuples representing the relationships between the duplicate
        labels.
        """
        duplicates = [["A", "B", "C"], ["D", "E"]]
        expected_output = [
            ["+", "A", "B", 0],
            ["+", "A", "C", 0],
            ["+", "B", "C", 0],
            ["+", "D", "E", 0],
        ]
        self.assertEqual(list(format_duplicates(duplicates)), expected_output)

    def test_format_empty_input(self):
        """
        Test that `format_duplicates` correctly handles an empty list
        of duplicate labels.

        The test case checks that `format_duplicates` returns an empty
        list when given an empty list of duplicate labels.
        """
        self.assertEqual(list(format_duplicates([])), [])


if __name__ == "__main__":
    unittest.main()
