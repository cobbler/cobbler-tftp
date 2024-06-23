# vim: ft=dockerfile
# Define the names/tags of the container
#!BuildTag: cobbler-test-github:release33 cobbler-test-github:release33.%RELEASE%

# We are using https://github.com/hadolint/hadolint to lint our Dockerfile.
# We don't want to version pin our dependencies for testing. Always retrieve what is up to date.
# hadolint global ignore=DL3037

FROM opensuse/leap:15.6

# Define labels according to https://en.opensuse.org/Building_derived_containers
# labelprefix=org.opensuse.example
LABEL org.opencontainers.image.title="cobbler-tftp"
LABEL org.opencontainers.image.description="This image runs the (nearly) stateless Cobbler TFTP server."
LABEL org.opencontainers.image.version="release34.%RELEASE%"
LABEL org.opensuse.reference="registry.opensuse.org/systemsmanagement/cobbler/release34/cobbler-tftp:release34.%RELEASE%"
LABEL org.openbuildservice.disturl="%DISTURL%"
LABEL org.opencontainers.image.created="%BUILDTIME%"
# endlabelprefix

# ENV Variables we are using.
ENV container docker

# Custom repository
RUN zypper ar https://download.opensuse.org/repositories/systemsmanagement:/cobbler:/release34/15.6/ "Cobbler 3.4.x release project" \
    && zypper --gpg-auto-import-keys refresh

# Dev Dependencies
RUN zypper in cobbler-tftp \
    && zypper clean

EXPOSE 69/UDP
CMD ["cobbler-tftp", "--no-daemon"]
