import os
import tempfile
import unittest
from unittest.mock import Mock

from convert.src.convert import STRATEGY_MAP, main, read_args, validate_args
from convert.src.handlers.handler import Handler, Reader, Writer


class TestFileConversion(unittest.TestCase):
    def test_read_args(self):
        # Test that read_args returns the expected arguments
        args = read_args(
            [
                "-i",
                "input.csv",
                "-o",
                "output.txt",
                "-d",
                "data.txt",
                "-r",
                "duke",
                "-w",
                "dedupe",
            ]
        )
        self.assertEqual(args.input, "input.csv")
        self.assertEqual(args.output, "output.txt")
        self.assertEqual(args.data, "data.txt")
        self.assertEqual(args.reader, "duke")
        self.assertEqual(args.writer, "dedupe")

    def test_validate_args(self):
        # Test that validate_args raises the expected errors
        with self.assertRaises(FileExistsError):
            validate_args(Mock(input="input.csv", output="output.txt", data="data.txt"))
        with self.assertRaises(FileNotFoundError):
            validate_args(
                Mock(input="nonexistent.csv", output="output.txt", data="data.txt")
            )
        with self.assertRaises(PermissionError):
            validate_args(
                Mock(input="input.csv", output="/root/output.txt", data="data.txt")
            )

    def test_file_conversion(self):
        # Test the main file conversion functionality
        # Create a temporary input file
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as input_file:
            input_file.write("1,2,3\n4,5,6\n")

        # Create a temporary data file
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as data_file:
            data_file.write("duke,dedupe\n")

        # Define the expected output
        expected_output = "1,2,3\nduke\n4,5,6\ndedupe\n"

        # Perform the conversion
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as output_file:
            main(
                [
                    "-i",
                    input_file.name,
                    "-o",
                    output_file.name,
                    "-d",
                    data_file.name,
                    "-r",
                    "duke",
                    "-w",
                    "dedupe",
                ]
            )

            # Assert that the output file contains the expected data
            output_file.seek(0)
            self.assertEqual(output_file.read(), expected_output)

        # Clean up the temporary files
        os.unlink(input_file.name)
        os.unlink(data_file.name)

    def test_strategy_map(self):
        # Test that all strategies defined in the STRATEGY_MAP are valid
        for handler_class in STRATEGY_MAP.values():
            handler = handler_class()
            self.assertTrue(isinstance(handler, Handler))
            self.assertTrue(isinstance(handler, handler_class.Reader))
            self.assertTrue(isinstance(handler, handler_class.Writer))


if __name__ == "__main__":
    unittest.main()
