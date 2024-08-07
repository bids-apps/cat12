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
            validate=False,
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


def init_derivatives_layout(output_dir) -> BIDSLayout:
    """Initialize a derivatives dataset and returns its layout.

    :param output_dir:
    :type output_dir: Path

    :return:
    :rtype: BIDSLayout
    """
    create_dir_if_absent(output_dir)
    layout_out = get_dataset_layout(output_dir)
    layout_out = set_dataset_description(layout_out)
    layout_out.dataset_description["DatasetType"] = "derivative"
    layout_out.dataset_description["GeneratedBy"][0]["Name"] = "CAT12"
    write_dataset_description(layout_out)
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


def set_dataset_description(
    layout: BIDSLayout, is_derivative: bool = True
) -> BIDSLayout:
    """Add dataset description to a layout.

    :param layout: _description_
    :type layout: BIDSLayout

    :param is_derivative: Defaults to True
    :type is_derivative: bool, optional

    :return: Updated BIDSLayout of the dataset
    :rtype: BIDSLayout
    """
    data: dict[str, Any] = {
        "Name": "dataset name",
        "BIDSVersion": "1.9.0",
        "DatasetType": "raw",
        "License": "CCO",
        "Authors": ["", ""],
        "Acknowledgements": "Special thanks to: ",
        "HowToAcknowledge": """Please cite this paper: """,
        "Funding": ["", ""],
        "ReferencesAndLinks": [],
        "DatasetDOI": "doi:",
    }

    if is_derivative:
        data["GeneratedBy"] = [
            {
                "Name": "bidsMReye",
                "Version": __version__,
                "Container": {"Type": "", "Tag": ""},
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

    layout.dataset_description = data

    return layout


def write_dataset_description(layout: BIDSLayout) -> None:
    """Add a dataset_description.json to a BIDS dataset.

    :param layout: BIDSLayout of the dataset to update.
    :type layout: BIDSLayout
    """
    output_file = Path(layout.root) / "dataset_description.json"

    with open(output_file, "w") as ff:
        json.dump(layout.dataset_description, ff, indent=4)
