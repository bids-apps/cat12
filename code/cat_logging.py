"""For logging."""

from __future__ import annotations

import logging

from defaults import default_log_level
from rich.logging import RichHandler
from rich.traceback import install


def cat12_log(name: str | None = None, log_level: int = logging.INFO) -> logging.Logger:
    """Create log."""
    """Create log."""
    # let rich print the traceback
    install(show_locals=True)

    FORMAT = "cat12 - %(asctime)s - %(message)s"

    log_level = default_log_level()

    if not name:
        name = "rich"

    logging.basicConfig(
        level=log_level,
        format=FORMAT,
        datefmt="[%X]",
        handlers=[
            RichHandler(),
        ],
    )

    return logging.getLogger(name)
