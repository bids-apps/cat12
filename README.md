# CAT-12 container

Docker and Apptainer image for [CAT12](https://neuro-jena.github.io/cat/).

CAT12 8.1 r2042
SPM12, version 7771 (standalone)
MATLAB, version 9.3.0.713579 (R2017b)


## Usage notes


### Example

```bash
docker build . --tag cat12
```

```bash
docker run -v ${PWD}/tests/data/MoAEpilot:/data \
    --rm -it cat12 \
        /data/sub-01/anat/sub-01_T1w.nii \
        -b cat_standalone_segment.m
```
