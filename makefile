tests/data/MoAEpilot:
	mkdir -p tests/data
	curl -fL -o moae.zip https://www.fil.ion.ucl.ac.uk/spm/download/data/MoAEpilot/MoAEpilot.bids.zip
	unzip -q moae.zip -d tests/data
	rm -f moae.zip

build:
	docker build . --tag cat12

view:
	docker run --rm -it  -v $${PWD}/tests/data/MoAEpilot:/data --rm cat12 . . participant view tfce

copy:
	docker run --rm -it  -v $${PWD}/tests/data/MoAEpilot:/data --rm cat12 . /foo participant copy tfce

segment:
	docker run --rm -it  -v $${PWD}/tests/data/MoAEpilot:/data --rm cat12 /data /data/derivatives participant segment
