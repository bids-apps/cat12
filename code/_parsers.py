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
    )
    parser.add_argument(
        "-v",
        "--verbose",
        dest="log_level",
        action="append_const",
        const=-1,
    )
    parser.add_argument(
        "--bids_filter_file",
        help="""
A JSON file describing custom BIDS input filters using PyBIDS.
For further details, please check out TBD.
        """,
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

    return parser


# cat_standalone_segment_enigma.m
# cat_standalone_segment_long.m
# cat_standalone_resample.m
# cat_standalone_simple.m
# cat_standalone_tfce.m
# cat_standalone_get_IQR.m
# cat_standalone_smooth.m
# cat_standalone_dicom2nii.m
# cat_standalone_deface.m
# cat_standalone_get_TIV.m
# cat_standalone_segment.m
# cat_standalone_get_quality.m
# cat_standalone_get_ROI_values.m
