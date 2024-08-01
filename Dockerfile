FROM debian:bookworm-slim

LABEL org.opencontainers.image.authors="fil.spm@ucl.ac.uk, Malgorzata Wierzba (m.wierzba@fz-juelich.de), Felix Hoffstaedter (f.hoffstaedter@fz-juelich.de)"
LABEL org.opencontainers.image.source="https://gin.g-node.org/felixh/cat12-container"
LABEL org.opencontainers.image.version="v1.1"

ARG DEBIAN_FRONTEND="noninteractive"

ENV CATversion="r2560"
ENV STANDALONE="/opt/spm12/toolbox/cat12/standalone"

RUN apt-get update -qq && \
    apt-get -qq -y --no-install-recommends install \
    build-essential \
    ca-certificates \
    curl \
    unzip \
    liboctave-dev \
    libxext6 \
    libxt6 \
    moreutils \
    octave \
    wget \
 && apt-get clean \
 && rm -rf \
     /tmp/hsperfdata* \
     /var/*/apt/*/partial \
     /var/lib/apt/lists/* \
     /var/log/apt/term*

#  install SPM12
RUN mkdir /opt/spm12 \
    && curl -fsSL --retry 5 https://github.com/spm/spm12/archive/r7771.tar.gz | tar -xzC /opt/spm12 --strip-components 1 \
    && curl -fsSL --retry 5  https://raw.githubusercontent.com/spm/spm-octave/main/spm12_r7771.patch | patch -p0 \
    && make -C /opt/spm12/src PLATFORM=octave distclean \
    && make -C /opt/spm12/src PLATFORM=octave \
    && make -C /opt/spm12/src PLATFORM=octave install \
    && ln -s /opt/spm12/bin/spm12-octave /usr/local/bin/spm12

# transfer code and set permission
RUN mkdir -p /code
COPY ./code /code
RUN ls /code && find /code -type f -print0 | xargs -0 chmod +r

# install CAT12
RUN mkdir -p /batch \
    && mkdir -p /downloads \
    && cd /downloads \
    && wget http://www.neuro.uni-jena.de/cat12/cat12_${CATversion}.zip && unzip -d /opt/spm12/toolbox/ cat12_${CATversion}.zip \
    && rm -fr /downloads \
    && cd ${STANDALONE} && chmod +rx *.sh \
    && cd /code && ln -s ${STANDALONE}/*.sh . \
    && cd /batch && ln -s ${STANDALONE}/*.m .

# clean
RUN rm -f /opt/spm12/src/*.{mex,o,a}

ENTRYPOINT ['/code/main "$@"']
