tests/data/MoAEpilot:
	mkdir -p tests/data
	curl -fL -o moae.zip https://www.fil.ion.ucl.ac.uk/spm/download/data/MoAEpilot/MoAEpilot.bids.zip
	unzip -q moae.zip -d tests/data
	rm -f moae.zip
