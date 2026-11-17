# vim: ft=dockerfile

FROM rockylinux/rockylinux:10

RUN dnf makecache && \
    dnf install -y epel-release dnf-utils && \
    dnf config-manager --set-enabled crb && \
    dnf makecache

# Add the Cobbler 4.0.x release repository from OBS, which already publishes
# python3-fbtftp for Rocky Linux 10 (not yet in upstream EPEL/Rocky repos)
RUN dnf config-manager --add-repo https://download.opensuse.org/repositories/systemsmanagement:/cobbler:/release40/RockyLinux_10/systemsmanagement:cobbler:release40.repo && \
    dnf makecache

# Create work directory
WORKDIR /workspace
VOLUME /workspace

# overlay2 bug with yum/dnf: touch /var/lib/rpm/* before 'dnf install' to avoid rpmdb
# corruption, see cobbler/docker/rpms/Rocky_Linux_10/Rocky_Linux_10.dockerfile
RUN touch /var/lib/rpm/* &&    \
    dnf install -y             \
    rpm-build                  \
    epel-rpm-macros            \
    pyproject-rpm-macros       \
    python-rpm-macros          \
    systemd-rpm-macros         \
    python3                    \
    python3-devel              \
    python3-pip                \
    python3-setuptools         \
    python3-setuptools_scm     \
    python3-wheel              \
    python3-click              \
    python3-daemon             \
    python3-PyYAML             \
    python3-schema             \
    python3-fbtftp             \
    git                        \
    fdupes

# Set up RPM build directories
RUN mkdir -p ~/rpmbuild/{BUILD,RPMS,SOURCES,SPECS,SRPMS}

# Copy entrypoint script (shared with the other RPM builds - distro agnostic)
COPY ./docker/rpm/entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
