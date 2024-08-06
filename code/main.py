"""Run CAT12 BIDS app."""

import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from _parsers import common_parser
from cat_logging import cat12_log
from rich import print
from rich_argparse import RichHelpFormatter

logger = cat12_log(name="cat12")

argv = sys.argv

# Get environment variable
STANDALONE = Path(os.getenv("STANDALONE"))


def print_error_and_exit(message):
    """Log error and exit."""
    logger.error(message)
    #  print help
    subprocess.run([STANDALONE / "cat_standalone.sh"])
    sys.exit(1)


def main():
    """Run the app."""
    parser = common_parser(formatter_class=RichHelpFormatter)

    args = parser.parse_args(argv[1:])

    # bids_dir = args.bids_dir[0]
    # output_dir = args.output_dir[0]
    # analysis_level = args.analysis_level[0]
    command = args.command

    if command == "copy":
        target = args.target[0]
        destination: Path = Path(args.destination[0])

        destination.mkdir(exist_ok=True, parents=True)

        if target == "all":
            files = STANDALONE.glob("*.m")
        else:
            files = [STANDALONE / f"cat_standalone_{target}.m"]

        for source_file in files:
            logger.info(f"Copying {source_file} to {str(destination)}")
            shutil.copy(source_file, destination)

        sys.exit(0)

    elif command == "view":
        target = args.target[0]
        source_file = STANDALONE / f"cat_standalone_{target}.m"
        with source_file.open("r") as file:
            print(f"[green]{file.read()}")
        sys.exit(0)

    # Run CAT
    now = datetime.now().strftime("%s")
    log_file = Path(f"cat_{now}.log")
    with log_file.open("w") as log:
        subprocess.run(
            [STANDALONE / "cat_standalone.sh"] + sys.argv[1:],
            stdout=log,
            stderr=subprocess.STDOUT,
        )


if __name__ == "__main__":
    main()
