# vim: ft=dockerfile
# hadolint ignore=DL3006
FROM opensuse/tumbleweed

# Create work directory
WORKDIR /workspace
VOLUME /workspace

# Install required dependencies
RUN zypper ar https://download.opensuse.org/repositories/systemsmanagement:/cobbler:/release34/openSUSE_Tumbleweed/systemsmanagement:cobbler:release34.repo && \
    zypper -n --gpg-auto-import-keys refresh && \
    zypper -n install \
        rpm-build \
        python-rpm-macros \
        python313 \
        python313-pip \
        python313-setuptools \
        python313-setuptools_scm \
        python313-wheel \
        python313-build \
        python313-click \
        python313-python-daemon \
        python313-PyYAML \
        python313-importlib-metadata \
        python313-importlib-resources \
        python313-schema \
        python313-fbtftp \
        git \
        fdupes

# Set up RPM build directories
RUN mkdir -p ~/rpmbuild/{BUILD,RPMS,SOURCES,SPECS,SRPMS}

# Copy entrypoint script
COPY ./docker/rpm/entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
