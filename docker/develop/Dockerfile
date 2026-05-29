# vim: ft=dockerfile

FROM registry.opensuse.org/opensuse/tumbleweed

# Define labels according to https://en.opensuse.org/Building_derived_containers
# labelprefix=org.opensuse.example
LABEL org.opencontainers.image.title="cobbler-tftp"
LABEL org.opencontainers.image.description="This image runs the (nearly) stateless Cobbler TFTP server."
LABEL org.opencontainers.image.version="dev.%RELEASE%"
LABEL org.opensuse.reference="registry.opensuse.org/systemsmanagement/cobbler/dev/cobbler-tftp:dev.%RELEASE%"
LABEL org.openbuildservice.disturl="%DISTURL%"
LABEL org.opencontainers.image.created="%BUILDTIME%"
# endlabelprefix

# ENV Variables we are using.
ENV container=docker
ENV COBBLER_TFTP__TFTP__PORT=6969

# Custom repository
RUN zypper ar https://download.opensuse.org/repositories/systemsmanagement:/cobbler:/release34/openSUSE_Tumbleweed/ "Cobbler 3.4.x release project" \
    && zypper --gpg-auto-import-keys refresh

# Dependencies
RUN zypper in -y git \
    python3-devel \
    python3-pip \
    && zypper clean

WORKDIR /code
EXPOSE 6969/udp
USER 1000
CMD ["/code/docker/develop/entrypoint.sh"]
