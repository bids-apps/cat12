"""For logging."""

from __future__ import annotations

import logging

from rich.logging import RichHandler
from rich.traceback import install


def cat12_log(name: str | None = None) -> logging.Logger:
    """Create log."""
    # let rich print the traceback
    install(show_locals=True)

    FORMAT = "cat12 - %(asctime)s - %(message)s"

    if not name:
        name = "rich"

    logging.basicConfig(
        level="INFO",
        format=FORMAT,
        datefmt="[%X]",
        handlers=[
            RichHandler(),
        ],
    )

    return logging.getLogger(name)
