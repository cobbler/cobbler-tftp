# vim: ft=dockerfile
# hadolint ignore=DL3006
#
# Build target for openSUSE Leap 16.0 / SLES 16.0 RPMs. Mirrors
# docker/rpm/openSUSE_tumbleweed/Dockerfile but targets Leap 16.0, the
# release target distro for Cobbler 4.0.x.
FROM registry.opensuse.org/opensuse/leap:16.0

# Create work directory
WORKDIR /workspace
VOLUME /workspace

# Add the Cobbler 4.0.x release repository from OBS, which already publishes
# python3-fbtftp for Leap 16.0 (not yet in upstream Leap repos)
RUN zypper ar -f https://download.opensuse.org/repositories/systemsmanagement:/cobbler:/release40/16.0/ systemsmanagement:cobbler:release40 && \
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

# Copy entrypoint script (shared with the Tumbleweed build - distro agnostic)
COPY ./docker/rpm/entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
