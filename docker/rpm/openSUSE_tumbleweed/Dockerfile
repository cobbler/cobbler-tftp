# vim: ft=dockerfile
# hadolint ignore=DL3006
FROM registry.opensuse.org/opensuse/tumbleweed

# Create work directory
WORKDIR /workspace
VOLUME /workspace

# Install required dependencies
RUN zypper ar https://download.opensuse.org/repositories/systemsmanagement:/cobbler:/release40/openSUSE_Tumbleweed/systemsmanagement:cobbler:release40.repo && \
    zypper -n --gpg-auto-import-keys refresh && \
    zypper -n install \
    rpm-build \
    python-rpm-macros \
    python3 \
    python3-devel \
    python3-pip \
    python3-setuptools \
    python3-setuptools_scm \
    python3-wheel \
    python3-build \
    python3-click \
    python3-python-daemon \
    python3-PyYAML \
    python3-importlib-metadata \
    python3-importlib-resources \
    python3-schema \
    python3-fbtftp \
    git \
    fdupes

# Set up RPM build directories
RUN mkdir -p ~/rpmbuild/{BUILD,RPMS,SOURCES,SPECS,SRPMS}

# Copy entrypoint script
COPY ./docker/rpm/entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
