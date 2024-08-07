"""BIDS utilities."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from _version import __version__
from bids import BIDSLayout  # type: ignore
from cat_logging import cat12_log
from utils import create_dir_if_absent

logger = cat12_log(name="cat12")


def get_dataset_layout(
    dataset_path: str | Path,
    use_database: bool = False,
    reset_database: bool = False,
) -> BIDSLayout:
    """Return a BIDSLayout object for the dataset at the given path.

    :param dataset_path: Path to the dataset.
    :type dataset_path: Union[str, Path]

    :param use_database: Defaults to False
    :type use_database: bool, optional

    :return: _description_
    :rtype: BIDSLayout
    """
    if isinstance(dataset_path, str):
        dataset_path = Path(dataset_path)

    dataset_path = dataset_path.absolute()

    logger.info(f"indexing {dataset_path}")

    if not use_database:
        return BIDSLayout(
            dataset_path,
            validate=True,
            derivatives=False,
        )

    database_path = dataset_path / "pybids_db"
    return BIDSLayout(
        dataset_path,
        validate=False,
        derivatives=False,
        database_path=database_path,
        reset_database=reset_database,
    )


def init_derivatives_layout(output_dir: Path) -> BIDSLayout:
    """Initialize a derivatives dataset and returns its layout.

    :param output_dir:
    :type output_dir: Path

    :return:
    :rtype: BIDSLayout
    """
    create_dir_if_absent(output_dir)
    write_dataset_description(output_dir)
    layout_out = get_dataset_layout(output_dir)
    return layout_out


def list_subjects(layout: BIDSLayout, subjects) -> list[str]:
    """List subject in a BIDS dataset for a given Config.

    :param cfg: Configuration object
    :type cfg: Config

    :param layout: BIDSLayout of the dataset.
    :type layout: BIDSLayout

    :raises RuntimeError: _description_

    :return: _description_
    :rtype: list
    """
    subjects = layout.get(return_type="id", target="subject", subject=subjects)

    if subjects == [] or subjects is None:
        raise RuntimeError(f"No subject found in layout:\n\t{layout.root}")

    logger.info(f"processing subjects: {subjects}")

    return subjects


def write_dataset_description(output_dir) -> None:
    """Add dataset description to a layout.

    :param output_dir: output_dir
    :type output_dir: Path
    """
    data: dict[str, Any] = {
        "Name": "dataset name",
        "BIDSVersion": "1.9.0",
        "DatasetType": "derivative",
        "License": "???",
        "ReferencesAndLinks": ["https://doi.org/10.1101/2022.06.11.495736"],
    }
    data["GeneratedBy"] = [
        {
            "Name": "cat12",
            "Version": __version__,
            "Container": {"Type": "", "Tag": __version__},
            "Description": "",
            "CodeURL": "",
        },
    ]
    data["SourceDatasets"] = [
        {
            "DOI": "doi:",
            "URL": "",
            "Version": "",
        }
    ]

    output_file = output_dir / "dataset_description.json"

    with open(output_file, "w") as ff:
        json.dump(data, ff, indent=4)
