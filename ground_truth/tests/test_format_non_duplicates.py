import unittest

from src.gt import format_non_duplicates


class TestFormatNonDuplicates(unittest.TestCase):
    """Test case for the `format_non_duplicates` function."""

    def test_format_non_duplicates(self):
        """Test the `format_non_duplicates` function.

        Check that the obtained output is equivalent to the expected output,
        regardless of the order of the elements.
        """
        duplicates = [["A", "B", "C"], ["D", "E"]]
        uniques = ["F", "G"]
        expected_output = [
            ["-", "A", "F", 0],
            ["-", "A", "G", 0],
            ["-", "A", "D", 0],
            ["-", "A", "E", 0],
            ["-", "B", "F", 0],
            ["-", "B", "G", 0],
            ["-", "B", "D", 0],
            ["-", "B", "E", 0],
            ["-", "C", "F", 0],
            ["-", "C", "G", 0],
            ["-", "C", "D", 0],
            ["-", "C", "E", 0],
            ["-", "D", "F", 0],
            ["-", "D", "G", 0],
            ["-", "E", "F", 0],
            ["-", "E", "G", 0],
            ["-", "F", "G", 0],
        ]

        obtained = format_non_duplicates(duplicates, uniques)
        for element in obtained:
            equivalent = element.copy()
            equivalent[1], equivalent[2] = equivalent[2], equivalent[1]

            self.assertTrue(
                (element in expected_output) or (equivalent in expected_output)
            )


if __name__ == "__main__":
    unittest.main()
