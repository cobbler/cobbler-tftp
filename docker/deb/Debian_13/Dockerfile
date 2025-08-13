# vim: ft=dockerfile
FROM docker.io/library/debian:trixie

ENV DEBIAN_FRONTEND=noninteractive

# Create work directory
WORKDIR /workspace
VOLUME /workspace

# hadolint ignore=DL3008
RUN apt-get update -qq && \
    apt-get install --no-install-recommends -qqy \
    build-essential  \
    debhelper  \
    devscripts \
    dh-python  \
    git \
    python3-setuptools  \
    python3-pip  \
    python3-setuptools-scm  \
    python3-pytest  \
    python3-schema  \
    python3-daemon  \
    python3-yaml  \
    python3-click  \
    python3-fbtftp  \
    python3-pytest-mock && \
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Copy entrypoint script
COPY ./docker/deb/entrypoint.sh /entrypoint.sh

# Make directory for debs
RUN mkdir -p /usr/src/cobbler-tftp/deb-build
VOLUME /usr/src/cobbler-tftp/deb-build

ENTRYPOINT ["/entrypoint.sh"]
