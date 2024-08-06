"""Store defaults."""

from __future__ import annotations


def default_log_level() -> str:
    """Return default log level."""
    return "INFO"


def log_levels() -> list[str]:
    """Return a list of log levels."""
    return ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


def supported_batches() -> list[str]:
    """List of batches supported by the app."""
    return [
        "segment_enigma",
        "segment_long",
        "resample",
        "simple",
        "tfce",
        "get_IQR",
        "smooth",
        "get_TIV",
        "segment",
        "get_quality",
        "get_ROI_values",
    ]
