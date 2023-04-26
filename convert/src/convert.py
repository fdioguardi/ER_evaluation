"""
Convert a file from one format to another using the specified reader
and writer strategies.
"""

import argparse
import errno
import os
from typing import Final

from handlers.dedupe import DedupeHandler
from handlers.duke import DukeHandler
from handlers.handler import Handler, Reader, Writer
from handlers.jedai import JedaiHandler

STRATEGY_MAP: Final[dict[str, Handler.__class__]] = {
    "duke": DukeHandler,
    "dedupe": DedupeHandler,
    "jedai": JedaiHandler,
}


def main() -> None:
    """Parse command-line arguments and execute the conversion process."""
    args: argparse.Namespace = read_args()

    validate_args(args)

    reader: Reader = STRATEGY_MAP[args.reader]()
    writer: Writer = STRATEGY_MAP[args.writer]()
    writer.write(
        filename=args.output,
        datafile=args.data,
        duplicates=reader.read_dups(args.input),
        non_dups=reader.read_non_dups(args.input),
    )


def validate_args(args: argparse.Namespace) -> None:
    """
    Validate command line arguments.

    Args:
        args (argparse.Namespace): Command-line arguments.

    Raises:
        FileExistsError: If the output file already exists.
        FileNotFoundError: If the input or data file do not exist.
        PermissionError: If the user does not have the required
            permissions to access a file.
    """
    if os.path.isfile(args.output):
        raise FileExistsError(errno.EEXIST, os.strerror(errno.EEXIST), args.output)

    if not os.path.isdir(os.path.dirname(args.output)):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), args.output)

    if not os.access(os.path.dirname(args.output), os.W_OK):
        raise PermissionError(errno.EACCES, os.strerror(errno.EACCES), args.output)

    for file in [args.input, args.data]:
        if not os.path.isfile(file):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), file)

        if not os.access(file, os.R_OK):
            raise PermissionError(errno.EACCES, os.strerror(errno.EACCES), file)


def read_args() -> argparse.Namespace:
    """
    Parse command-line arguments.

    Returns:
        An argparse.Namespace containing the parsed command-line
        arguments.
    """
    parser: argparse.ArgumentParser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "-i", "--input", type=str, required=True, help="The input file to convert."
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        required=True,
        help="The output file to write to. If this file already exists, a FileExistsError will be raised.",
    )
    parser.add_argument(
        "-d", "--data", type=str, required=True, help="The data file to read."
    )
    parser.add_argument(
        "-r",
        "--reader",
        choices=sorted(STRATEGY_MAP.keys()),
        type=str,
        required=True,
        help="The reader strategy to use for the conversion.",
    )
    parser.add_argument(
        "-w",
        "--writer",
        choices=sorted(STRATEGY_MAP.keys()),
        type=str,
        required=True,
        help="The writer strategy to use for the conversion.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    main()
