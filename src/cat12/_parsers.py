from __future__ import annotations

from argparse import ArgumentParser, HelpFormatter

from cat12._version import __version__

from cat12.defaults import CAT_VERSION, MCR_VERSION, supported_batches


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
        version=f"""
        BIDS app: {__version__};
        CAT12: {CAT_VERSION};
        MATLAB MCR: {MCR_VERSION}
""",
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
    parser = _add_verbose(parser)
    parser.add_argument(
        "--bids_filter_file",
        help="""
A JSON file describing custom BIDS input filters using PyBIDS.
For further details, please check out TBD.
        """,
        required=False,
    )
    parser.add_argument(
        "--skip_validation",
        help="Do not run the bids validation.",
        action="store_true",
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


def _add_verbose(parser):
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
    view_parser = _add_verbose(view_parser)

    copy_parser = subparsers.add_parser(
        "copy",
        help="Copy batch to output_dir.",
        formatter_class=parser.formatter_class,
    )
    copy_parser = _add_target(copy_parser, with_all=True)
    copy_parser = _add_verbose(copy_parser)

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
 simple: simple processing batch;
 long_0 - longitudinal developmental;
 long_1 - longitudinal plasticity/learning;
 long_2 - longitudinal aging;
 long_3 - longitudinal save models 1 and 2;
 enigma - enigma segmentation
""",
        choices=[
            "default",
            "simple",
            "long_0",
            "long_1",
            "long_2",
            "long_3",
            "enigma",
        ],
        default="default",
        required=False,
        type=str,
        nargs=1,
    )

    return parser
