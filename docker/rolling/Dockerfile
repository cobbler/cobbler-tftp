# vim: ft=dockerfile
# Define the names/tags of the container
#!BuildTag: cobbler-test-github:release33 cobbler-test-github:release33.%RELEASE%

# We are using https://github.com/hadolint/hadolint to lint our Dockerfile.
# We don't want to version pin our dependencies for testing. Always retrieve what is up to date.
# hadolint global ignore=DL3037

FROM opensuse/tumbleweed:latest

# Define labels according to https://en.opensuse.org/Building_derived_containers
# labelprefix=org.opensuse.example
LABEL org.opencontainers.image.title="cobbler-tftp"
LABEL org.opencontainers.image.description="This image runs the (nearly) stateless Cobbler TFTP server."
LABEL org.opencontainers.image.version="rolling.%RELEASE%"
LABEL org.opensuse.reference="registry.opensuse.org/systemsmanagement/cobbler/containers/cobbler-tftp:rolling.%RELEASE%"
LABEL org.openbuildservice.disturl="%DISTURL%"
LABEL org.opencontainers.image.created="%BUILDTIME%"
# endlabelprefix

# ENV Variables we are using.
ENV container docker

# Custom repository
RUN zypper ar https://download.opensuse.org/repositories/systemsmanagement:/cobbler:/release34/openSUSE_Tumbleweed/ "Cobbler 3.4.x release project" \
    && zypper --gpg-auto-import-keys refresh

# Dependencies
RUN zypper in -y cobbler-tftp \
    && zypper clean

EXPOSE 69/UDP
CMD ["cobbler-tftp", "start", "--no-daemon"]
