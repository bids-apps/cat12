tests/data/MoAEpilot:
	mkdir -p tests/data
	curl -fL -o moae.zip https://www.fil.ion.ucl.ac.uk/spm/download/data/MoAEpilot/MoAEpilot.bids.zip
	unzip -q moae.zip -d tests/data
	rm -f moae.zip

build:
	docker build . --tag cat12

view:
	docker run --rm -it cat12 . . participant view tfce

copy:
	docker run --rm -it cat12 . /foo participant copy tfce

segment: tests/data/MoAEpilot
	docker run --rm -it -v $${PWD}/tests/data/MoAEpilot:/data cat12 /data /data/derivatives participant segment


data_ds000001:
	mkdir -p tests/data
	cd tests/data && datalad install ///openneuro/ds000001
	cd tests/data/ds000001 && datalad get sub*/**/*T1w* -J 12

ds000001: data_ds000001
	mkdir -p tests/data/outputs
	docker run --rm \
		-v $${PWD}/tests/data:/data \
		cat12 /data/ds000001 /data/outputs/ds000001 participant segment --participant_label 01 02 03

data_ds002799:
	mkdir -p tests/data
	cd tests/data && datalad install ///openneuro/ds002799
	cd tests/data/ds002799 && datalad get sub-2*/*/*/*T1w* -J 12

ds002799: data_ds002799
	mkdir -p tests/data/outputs
	docker run --rm -it \
		-v $${PWD}/tests/data:/data \
		cat12 /data/ds002799 /data/outputs/ds002799 participant segment --participant_label 292 294
