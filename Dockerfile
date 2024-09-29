FROM ubuntu:22.04@sha256:340d9b015b194dc6e2a13938944e0d016e57b9679963fdeb9ce021daac430221

LABEL org.opencontainers.image.authors="fil.spm@ucl.ac.uk, Malgorzata Wierzba (m.wierzba@fz-juelich.de), Felix Hoffstaedter (f.hoffstaedter@fz-juelich.de), Remi Gau (remi.gau@gmail.com)"
LABEL org.opencontainers.image.source="https://gin.g-node.org/felixh/cat12-container"
LABEL org.opencontainers.image.version="v1.1dev"
LABEL org.opencontainers.image.licenses="MIT"
LABEL org.opencontainers.image.title="cat12-container"

ENV LANG="en_US.UTF-8" \
    LC_ALL="en_US.UTF-8" \
    FORCE_SPMMCR="1" \
    SPM_HTML_BROWSER="0" \
    MCR_INHIBIT_CTF_LOCK="1" \
    MCR_VERSION="2017b"
ENV LD_LIBRARY_PATH="$LD_LIBRARY_PATH:/usr/lib/x86_64-linux-gnu:/opt/MCR-${MCR_VERSION}/v93/runtime/glnxa64:/opt/MCR-${MCR_VERSION}/v93/bin/glnxa64:/opt/MCR-${MCR_VERSION}/v93/sys/os/glnxa64:/opt/MCR-${MCR_VERSION}/v93/extern/bin/glnxa64" \
    MATLABCMD="/opt/MCR-${MCR_VERSION}/v93/toolbox/matlab" \
    XAPPLRESDIR="/opt//opt/MCR-${MCR_VERSION}/v93/x11/app-defaults" \
    MCRROOT="/opt/MCR-${MCR_VERSION}/v93" \
    CAT_VERSION=".8.1_r2042_R${MCR_VERSION}" \
    DENO_INSTALL="/root/.deno"
ENV SPMROOT="/opt/CAT12${CAT_VERSION}" \
    PATH="$DENO_INSTALL/bin:/opt/CAT12${CAT_VERSION}:$PATH" \
    STANDALONE="/opt/CAT12${CAT_VERSION}/standalone"

RUN apt-get update -qq \
    && apt-get install -y -q --no-install-recommends \
           apt-utils \
           bc \
           bzip2 \
           ca-certificates \
           curl \
           dbus-x11 \
           git \
           libncurses5 \
           libxext6 \
           libxmu6 \
           libxpm-dev \
           libxt6 \
           locales \
           openjdk-8-jre \
           python3 \
           pip \
           unzip \
    && rm -rf /var/lib/apt/lists/* \
    && sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen \
    && dpkg-reconfigure --frontend=noninteractive locales \
    && update-locale LANG="en_US.UTF-8" \
    && chmod 777 /opt && chmod a+s /opt

RUN echo "Downloading MATLAB Compiler Runtime ..." \
    && export TMPDIR="$(mktemp -d)" \
    && curl  -o "$TMPDIR/mcr.zip" https://ssd.mathworks.com/supportfiles/downloads/R${MCR_VERSION}/deployment_files/R${MCR_VERSION}/installers/glnxa64/MCR_R${MCR_VERSION}_glnxa64_installer.zip \
    && unzip -q "$TMPDIR/mcr.zip" -d "$TMPDIR/mcrtmp" \
    && "$TMPDIR/mcrtmp/install" -destinationFolder /opt/MCR-${MCR_VERSION} -mode silent -agreeToLicense yes \
    && rm -rf "$TMPDIR" \
    && unset TMPDIR

RUN echo "Downloading standalone CAT12 ..." \
    && curl -fL -o /tmp/cat12.zip http://www.neuro.uni-jena.de/cat12/CAT12${CAT_VERSION}_MCR_Linux.zip \
    && unzip -q /tmp/cat12.zip -d /tmp \
    && rm -rf /tmp/cat12.zip \
    && mkdir -p /opt/CAT12${CAT_VERSION} \
    && mv /tmp/*${CAT_VERSION}*/* /opt/CAT12${CAT_VERSION}/ \
    && chmod -R 777 /opt/CAT12${CAT_VERSION} \
    # Test
    && /opt/CAT12${CAT_VERSION}/spm12 function exit

## Install BIDS validator
RUN curl -fsSL https://deno.land/install.sh | sh && \
    deno install -Agf -n bids-validator jsr:@bids/validator@1.14.12

# transfer code and set permission
RUN mkdir -p /code
COPY . /code
RUN cd code && \
    git restore . && \
    pip install -r requirements.txt && \
    pip install .

RUN ls /code && find /code -type f -print0 | xargs -0 chmod +r

# modify enigma script to output content to path defined by an env variable
RUN sed -i -e "s/cat_version/getenv('OUTPUT_DIR')/g" /opt/CAT12${CAT_VERSION}/standalone/cat_standalone_segment_enigma.m

WORKDIR ${STANDALONE}

ENTRYPOINT ["cat12"]
