# CAT-12 container

Docker and Apptainer image for [CAT12](https://neuro-jena.github.io/cat/).

CAT12 8.1 r2042
SPM12, version 7771 (standalone)
MATLAB, version 9.3.0.713579 (R2017b)


## Usage notes

```text
Usage: main.py [-h] [--version] bids_dir output_dir {participant,group} {view,copy,segment} ...

BIDS app for CAT12.

Positional Arguments:
  bids_dir             Fullpath to the directory with the input dataset formatted according to the BIDS standard.
  output_dir           Fullpath to the directory where the output files will be stored.
  {participant,group}  Level of the analysis that will be performed. Multiple participant level analyses can be run independently (in parallel)
                       using the same ``output_dir``.
  {view,copy,segment}  Choose a sub-command
    view               View batch.
    copy               Copy batch to output_dir.
    segment            segment

Options:
  -h, --help           show this help message and exit
  --version            Show program's version number and exit.
```

```text
Usage: main.py bids_dir output_dir {participant,group} segment [-h]
                                                                                                   [--participant_label PARTICIPANT_LABEL [PARTICIPANT_LABEL ...]]
                                                                                                   [--run RUN [RUN ...]] [-v]
                                                                                                   [--bids_filter_file BIDS_FILTER_FILE]

Options:
  -h, --help            show this help message and exit
  --participant_label PARTICIPANT_LABEL [PARTICIPANT_LABEL ...]
                        The label(s) of the participant(s) that should be analyzed. The label corresponds to sub-<participant_label> from the BIDS
                        spec (so it does not include "sub-"). If this parameter is not provided, all subjects will be analyzed. Multiple
                        participants can be specified with a space separated list.
  --run RUN [RUN ...]   The label of the run that will be analyzed. The label corresponds to run-<task_label> from the BIDS spec so it does not
                        include "run-").
  -v, --verbose
  --bids_filter_file BIDS_FILTER_FILE
                        A JSON file describing custom BIDS input filters using PyBIDS. For further details, please check out TBD.
```
