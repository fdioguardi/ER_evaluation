import argparse
from typing import Final

from convert.handlers.dedupe import DedupeHandler
from convert.handlers.duke import DukeHandler
from convert.handlers.handler import Reader, Writer
from convert.handlers.jedai import JedaiHandler

STRATEGY_MAP: Final = {
    "duke": DukeHandler,
    "dedupe": DedupeHandler,
    "jedai": JedaiHandler,
}


def main() -> None:
    args: argparse.Namespace = read_args()
    reader: Reader = STRATEGY_MAP[args.reader]()
    writer: Writer = STRATEGY_MAP[args.writer]()
    writer.write(args.output, reader.read(args.input))


def read_args() -> argparse.Namespace:
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Convert a file from one format to another."
    )
    parser.add_argument(
        "-i",
        "--input",
        type=str,
        required=True,
        help="The input file to convert.",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        required=True,
        help="The output file to write to.",
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
