from __future__ import annotations

from argparse import ArgumentParser, HelpFormatter

from _version import __version__
from defaults import supported_batches


def _base_parser(
    formatter_class: type[HelpFormatter] = HelpFormatter,
) -> ArgumentParser:
    parser = ArgumentParser(
        description=("BIDS app for CAT12."),
        formatter_class=formatter_class,
    )
    parser.add_argument(
        "--version",
        action="version",
        help="Show program's version number and exit.",
        version=f"cat12 bids app version {__version__}",
    )
    parser.add_argument(
        "bids_dir",
        help="""
Fullpath to the directory with the input dataset
formatted according to the BIDS standard.
        """,
        nargs=1,
    )
    parser.add_argument(
        "output_dir",
        help="""
Fullpath to the directory where the output files will be stored.
""",
        nargs=1,
    )
    parser.add_argument(
        "analysis_level",
        help="""
        Level of the analysis that will be performed.
        Multiple participant level analyses can be run independently
        (in parallel) using the same ``output_dir``.
        """,
        choices=["participant", "group"],
        default="participant",
        type=str,
        nargs=1,
    )

    return parser


def _add_common_arguments(parser: ArgumentParser) -> ArgumentParser:
    parser.add_argument(
        "--participant_label",
        help="""
The label(s) of the participant(s) that should be analyzed.
The label corresponds to sub-<participant_label> from the BIDS spec
(so it does not include "sub-").

If this parameter is not provided, all subjects will be analyzed.
Multiple participants can be specified with a space separated list.
        """,
        nargs="+",
        required=False,
    )
    parser.add_argument(
        "--verbose",
        help="""
        Verbosity level.
        """,
        choices=[0, 1, 2, 3],
        default=2,
        type=int,
        nargs=1,
    )
    parser.add_argument(
        "--bids_filter_file",
        help="""
A JSON file describing custom BIDS input filters using PyBIDS.
For further details, please check out TBD.
        """,
        required=False,
    )
    return parser


def _add_target(parser, with_all=False):
    choices = supported_batches()
    if with_all:
        choices.append("all")
    parser.add_argument(
        "target",
        help="Batch name",
        choices=supported_batches(),
        type=str,
        nargs=1,
    )
    return parser


def common_parser(
    formatter_class: type[HelpFormatter] = HelpFormatter,
) -> ArgumentParser:
    """Execute the main script."""
    parser = _base_parser(formatter_class=formatter_class)
    subparsers = parser.add_subparsers(
        dest="command",
        help="Choose a sub-command",
        required=True,
    )

    subparsers.add_parser(
        "help",
        help="Show cat12 script help.",
        formatter_class=parser.formatter_class,
    )

    view_parser = subparsers.add_parser(
        "view",
        help="View batch.",
        formatter_class=parser.formatter_class,
    )
    view_parser = _add_target(view_parser)

    copy_parser = subparsers.add_parser(
        "copy",
        help="Copy batch to output_dir.",
        formatter_class=parser.formatter_class,
    )
    copy_parser = _add_target(copy_parser, with_all=True)

    segment_parser = subparsers.add_parser(
        "segment",
        help="segment",
        formatter_class=parser.formatter_class,
    )
    segment_parser = _add_common_arguments(segment_parser)
    segment_parser.add_argument(
        "--reset_database",
        help="Resets the database of the input dataset.",
        action="store_true",
        required=False,
    )
    segment_parser.add_argument(
        "--type",
        help="""Type of segmentation.
 default: default CAT12 preprocessing batch;
 default: simple processing batch;
 0 - longitudinal developmental;
 1 - longitudinal plasticity/learning;
 2 - longitudinal aging;
 3 - longitudinal save models 1 and 2;
""",
        choices=["default", "simple", "0", "1", "2", "3"],
        default="default",
        required=False,
        type=str,
        nargs=1,
    )

    return parser
