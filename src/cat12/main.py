"""Run CAT12 BIDS app."""

import json
import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from subprocess import PIPE, STDOUT, Popen

import nibabel as nib
from cat12._version import __version__
from rich import print
from rich_argparse import RichHelpFormatter

from cat12._parsers import common_parser
from cat12.bids_utils import (
    get_dataset_layout,
    init_derivatives_layout,
    list_subjects,
)
from cat12.cat_logging import cat12_log
from cat12.defaults import CAT_VERSION, log_levels
from cat12.methods import generate_method_section
from cat12.utils import progress_bar

env = os.environ
env["PYTHONUNBUFFERED"] = "True"

argv = sys.argv

with Path.open(Path(__file__).parent / "exit_codes.json") as f:
    EXIT_CODES = json.load(f)

# Get environment variable
STANDALONE = os.getenv("STANDALONE")
if STANDALONE is None:
    STANDALONE = f"/opt/CAT12${CAT_VERSION}/standalone"
STANDALONE = Path(STANDALONE)

logger = cat12_log(name="cat12")


def main():
    """Run the app."""
    parser = common_parser(formatter_class=RichHelpFormatter)

    args = parser.parse_args(argv[1:])

    verbose = args.verbose
    if isinstance(verbose, list):
        verbose = verbose[0]

    log_level_name = log_levels()[int(verbose)]
    logger.setLevel(log_level_name)

    output_dir = Path(args.output_dir[0])

    command = args.command

    if command == "copy":
        target = args.target[0]

        output_dir.mkdir(exist_ok=True, parents=True)

        files = (
            STANDALONE.glob("*.m")
            if target == "all"
            else [STANDALONE / f"cat_standalone_{target}.m"]
        )
        for source_file in files:
            logger.info(f"Copying {source_file} to {output_dir!s}")
            shutil.copy(source_file, output_dir)

        sys.exit(EXIT_CODES["SUCCESS"]["Value"])

    elif command == "help":
        subprocess.run([STANDALONE / "cat_standalone.sh"])
        sys.exit(EXIT_CODES["SUCCESS"]["Value"])

    elif command == "view":
        target = args.target[0]
        source_file = STANDALONE / f"cat_standalone_{target}.m"
        with source_file.open("r") as file:
            print(f"[green]{file.read()}")

        sys.exit(EXIT_CODES["SUCCESS"]["Value"])

    bids_dir = Path(args.bids_dir[0])
    if not bids_dir.exists():
        logger.error(
            f"The following 'bids_dir' could not be found:\n{bids_dir}"
        )
        sys.exit(EXIT_CODES["DATAERR"]["Value"])

    if not args.skip_validation:
        run_validation(bids_dir)

    layout_in = get_dataset_layout(bids_dir)

    subjects = args.participant_label or layout_in.get_subjects()
    subjects = list_subjects(layout_in, subjects)

    analysis_level = args.analysis_level[0]
    if analysis_level == "group":
        logger.error("'group' level analysis not implemented yet.")
        sys.exit(EXIT_CODES["FAILURE"]["Value"])

    if command == "segment":
        segment_type = args.type
        if isinstance(segment_type, list):
            segment_type = segment_type[0]

        output_dir = output_dir / f"CAT12_{__version__}"

        if segment_type != "enigma":
            copy_files(layout_in, output_dir, subjects)
            layout_out = init_derivatives_layout(output_dir)
        else:
            os.environ["OUTPUT_DIR"] = os.path.relpath(output_dir, bids_dir)
            layout_out = layout_in

        batch = define_batch(segment_type=segment_type)

        logger.info(f"{segment_type=} - using batch {batch}.")

        (output_dir / "logs").mkdir(exist_ok=True, parents=True)
        shutil.copy2(
            src=Path("/opt")
            / f"CAT12{os.environ['CAT_VERSION']}"
            / "standalone"
            / batch,
            dst=output_dir / "logs",
        )

        generate_method_section(output_dir=output_dir, batch=batch)

        text = "processing subjects"
        with progress_bar(text=text) as progress:
            subject_loop = progress.add_task(
                description="processing subjects", total=len(subjects)
            )

            for subject_label in subjects:
                this_filter = {
                    "datatype": "anat",
                    "suffix": "T1w",
                    "extension": "nii",
                    "subject": subject_label,
                }

                bf = layout_out.get(
                    **this_filter,
                )

                if not check_input(subject_label, bf, segment_type):
                    continue

                log_file = log_filename(output_dir, subject_label)

                cmd = [str(STANDALONE / "cat_standalone.sh")]

                with log_file.open("w") as log:
                    if segment_type in ["default", "simple", "enigma"]:
                        for file in bf:
                            cmd.extend([file.path, "-b", batch])
                            run_command(cmd, log)

                    elif is_longitudinal_segmentation(segment_type):
                        # TODO do a mean for each time point first
                        files_to_process = [file.path for file in bf]
                        cmd.extend(files_to_process)
                        cmd.extend(["-b", batch, "-a1", segment_type[-1]])
                        run_command(cmd, log)

                gunzip_all_niftis(
                    output_dir=output_dir, subject_label=subject_label
                )

                progress.update(subject_loop, advance=1)

    sys.exit(EXIT_CODES["SUCCESS"]["Value"])


def check_input(subject_label: str, bf: list, segment_type: str):
    """Check number of input files."""
    if not bf:
        logger.warning(f"No data found for subject {subject_label}.")
        return False
    if is_longitudinal_segmentation(segment_type) and len(bf) < 2:
        logger.warning(
            "Longitudinal segmentation requested "
            f"but subject {subject_label} only has 1 image."
        )
    return True


def define_batch(segment_type):
    """Find batch to run."""
    batch = "cat_standalone_segment.m"
    if segment_type == "simple":
        batch = "cat_standalone_simple.m"
    elif is_longitudinal_segmentation(segment_type):
        batch = "cat_standalone_segment_long.m"
    elif segment_type == "enigma":
        batch = "cat_standalone_segment_enigma.m"
    return batch


def log_filename(output_dir, subject_label):
    """Generate filename for logfile."""
    now = datetime.now().replace(microsecond=0).isoformat()
    log_file = (
        output_dir
        / f"sub-{subject_label}"
        / "log"
        / f"{now}_sub-{subject_label}.log".replace(":", "_")
    )
    log_file.parent.mkdir(parents=True, exist_ok=True)
    return log_file


def is_longitudinal_segmentation(segment_type):
    """Check if the segmentation requested is longitudinal."""
    return segment_type in [
        "long_0",
        "long_1",
        "long_2",
        "long_3",
    ]


def run_command(cmd, log):
    """Run command and log to STDOUT and log."""
    logger.info(cmd)
    with Popen(
        cmd,
        stdout=PIPE,
        stderr=STDOUT,
        bufsize=1,
        text=True,
        encoding="utf-8",
        env=env,
    ) as proc:
        while (_ := proc.poll()) is None:
            line = proc.stdout.readline()
            sys.stdout.write(str(line))
            log.write(str(line))


def copy_files(layout_in, output_dir, subjects):
    """Copy input files to derivatives.

    SPM has the bad habit of dumping derivatives with the raw.
    Unzip files as SPM cannot deal with gz files.
    """
    text = "copying subjects"
    with progress_bar(text=text) as progress:
        copy_loop = progress.add_task(
            description="copying subjects", total=len(subjects)
        )
        for subject_label in subjects:
            logger.info(f"Copying {subject_label}")

            this_filter = {
                "datatype": "anat",
                "suffix": "T1w",
                "extension": "nii.*",
                "subject": subject_label,
            }
            bf = layout_in.get(
                **this_filter,
                regex_search=True,
            )
            for file in bf:
                output_filename = output_dir / file.relpath
                if output_filename.exists():
                    continue

                output_filename.parent.mkdir(exist_ok=True, parents=True)

                logger.info(f"Copying {file.path} to {output_dir!s}")
                img = nib.load(file.path)
                nib.save(img, output_filename)

            progress.update(copy_loop, advance=1)


def run_validation(bids_dir):
    """Run bids validator."""
    try:
        subprocess.run(f"bids-validator {bids_dir}", shell=True, check=True)
    except subprocess.CalledProcessError:
        sys.exit(EXIT_CODES["DATAERR"]["Value"])


def gunzip_all_niftis(output_dir: Path, subject_label: str):
    """Gunzip all niftis for a subject."""
    logger.info(f"Gunzipping files for {subject_label}")
    files = list((output_dir / f"sub-{subject_label}").glob("**/*.nii"))
    for f in files:
        nii = nib.load(f)
        nii.to_filename(f"{f!s}.gz")
        f.unlink()


if __name__ == "__main__":
    main()
