# vim: ft=dockerfile

FROM fedora:43

RUN dnf makecache

# Add the Cobbler 4.0.x release repository from OBS, which already publishes
# python3-fbtftp for Fedora 43 (not yet in upstream Fedora repos)
RUN dnf install -y dnf-plugins-core && \
    dnf config-manager addrepo --from-repofile https://download.opensuse.org/repositories/systemsmanagement:/cobbler:/release40/Fedora_43/systemsmanagement:cobbler:release40.repo

# Create work directory
WORKDIR /workspace
VOLUME /workspace

RUN dnf install -y           \
    rpm-build                \
    pyproject-rpm-macros     \
    systemd-rpm-macros       \
    python3-devel            \
    python3-pip              \
    python3-setuptools       \
    python3-setuptools_scm   \
    python3-wheel            \
    python3-click            \
    python3-daemon           \
    python3-PyYAML           \
    python3-schema           \
    python3-fbtftp           \
    git                      \
    fdupes

# Set up RPM build directories
RUN mkdir -p ~/rpmbuild/{BUILD,RPMS,SOURCES,SPECS,SRPMS}

# Copy entrypoint script (shared with the other RPM builds - distro agnostic)
COPY ./docker/rpm/entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
