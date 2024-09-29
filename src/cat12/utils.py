"""Utility functions."""

from __future__ import annotations

from pathlib import Path

from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    SpinnerColumn,
    TaskProgressColumn,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
)

from cat12.cat_logging import cat12_log

logger = cat12_log(name="cat12")


def progress_bar(text: str, color: str = "green") -> Progress:
    """Return a rich progress bar instance."""
    return Progress(
        TextColumn(f"[{color}]{text}"),
        SpinnerColumn("dots"),
        TimeElapsedColumn(),
        BarColumn(),
        MofNCompleteColumn(),
        TaskProgressColumn(),
        TimeRemainingColumn(),
    )


def create_dir_if_absent(output_path: str | Path) -> None:
    """Create a path if it does not exist.

    :param output_path:
    :type output_path: Union[str, Path]
    """
    if isinstance(output_path, str):
        output_path = Path(output_path)
    if not output_path.is_dir():
        logger.debug(f"Creating dir: {output_path}")
    output_path.mkdir(parents=True, exist_ok=True)
