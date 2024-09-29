"""Store defaults."""

from __future__ import annotations

import os

MCR_VERSION = os.getenv("MCR_VERSION")
if MCR_VERSION is None:
    MCR_VERSION = "2017b"

tmp = os.getenv("CAT_VERSION")
if tmp is None:
    tmp = f".8.1_r2042_R${MCR_VERSION}"
CAT_VERSION = " ".join(tmp[1:10].split("_"))


def log_levels() -> list[str]:
    """Return a list of log levels."""
    return ["ERROR", "WARNING", "INFO", "DEBUG"]


def supported_batches() -> list[str]:
    """List of batches supported by the app."""
    return [
        "segment",
        "simple",
        "segment_long",
        "segment_enigma",
        "resample",
        "get_IQR",
        "get_TIV",
        "get_quality",
        "get_ROI_values",
    ]


# cat_standalone_simple.m
# cat_standalone_segment.m
# cat_standalone_segment_enigma.m
# cat_standalone_segment_long.m

# cat_standalone_resample.m
# cat_standalone_get_IQR.m
# cat_standalone_get_TIV.m
# cat_standalone_get_quality.m
# cat_standalone_get_ROI_values.m

# WON'T DO
# cat_standalone_smooth.m
# cat_standalone_tfce.m
# cat_standalone_dicom2nii.m
# cat_standalone_deface.m
