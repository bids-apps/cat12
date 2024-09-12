"""Store defaults."""

from __future__ import annotations


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
        "tfce",
        "get_IQR",
        "smooth",
        "get_TIV",
        "get_quality",
        "get_ROI_values",
    ]


# cat_standalone_simple.m
# cat_standalone_segment.m
# cat_standalone_segment_enigma.m
# cat_standalone_segment_long.m

# cat_standalone_resample.m
# cat_standalone_tfce.m
# cat_standalone_get_IQR.m
# cat_standalone_smooth.m
# cat_standalone_get_TIV.m
# cat_standalone_get_quality.m
# cat_standalone_get_ROI_values.m

# WON'T DO
# cat_standalone_dicom2nii.m
# cat_standalone_deface.m
