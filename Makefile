DOCKER_IMAGE_NAME=cobbler-tftp-pkg
DOCKER_IMAGE_TAG_OCI=oci
DOCKER_IMAGE_TAG_DEV=develop
DOCKER_IMAGE_TAG_DEBIAN=debian-13
DOCKER_IMAGE_TAG_OPENSUSE_TW=opensuse-tumbleweed
DOCKER_IMAGE_TAG_OPENSUSE_LEAP16=opensuse-leap16
DOCKER_IMAGE_TAG_ROCKY10=rockylinux-10
DOCKER_IMAGE_TAG_FEDORA43=fedora-43

build:
	@python3 -m setuptools_scm --force-write-version-files
	@python3 -m pip wheel --verbose --use-pep517 --wheel-dir ./build .

container-image:
	@docker build -t localhost/${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG_OCI} -f docker/production/Dockerfile .

container-image-dev:
	@docker build -t localhost/${DOCKER_IMAGE_TAG_DEV} -f docker/develop/Dockerfile .
	@docker run --read-only -v .:/code:Z --tmpfs /venv:rw,exec localhost/${DOCKER_IMAGE_TAG_DEV}:latest

deb:
	@docker build -t localhost/${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG_DEBIAN} -f docker/deb/Debian_13/Dockerfile .
	@docker run --rm -v $(CURDIR)/debs/Debian_13:/usr/src/cobbler-tftp/deb-build:Z -v $(CURDIR):/workspace:Z localhost/${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG_DEBIAN}
	@docker run --rm -v $(CURDIR):/workspace:Z --entrypoint '' localhost/${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG_DEBIAN} bash -c 'dpkg -i /workspace/debs/Debian_13/cobbler-tftp*.deb'

rpm-tumbleweed:
	@docker build -t localhost/${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG_OPENSUSE_TW} -f docker/rpm/openSUSE_tumbleweed/Dockerfile .
	@docker run --rm -v $(CURDIR)/rpms/openSUSE_tumbleweed:/root/rpmbuild/RPMS:Z -v $(CURDIR):/workspace:Z localhost/${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG_OPENSUSE_TW}
	@docker run --rm -v $(CURDIR):/workspace:Z --entrypoint '' localhost/${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG_OPENSUSE_TW} rpm -i /workspace/rpms/openSUSE_tumbleweed/noarch/*.rpm

rpm-leap16:
	@docker build -t localhost/${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG_OPENSUSE_LEAP16} -f docker/rpm/openSUSE_Leap16/Dockerfile .
	@docker run --rm -v $(CURDIR)/rpms/openSUSE_Leap16:/root/rpmbuild/RPMS:Z -v $(CURDIR):/workspace:Z localhost/${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG_OPENSUSE_LEAP16}
	@docker run --rm -v $(CURDIR):/workspace:Z --entrypoint '' localhost/${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG_OPENSUSE_LEAP16} rpm -i /workspace/rpms/openSUSE_Leap16/noarch/*.rpm

rpm-rocky10:
	@docker build -t localhost/${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG_ROCKY10} -f docker/rpm/RockyLinux10/Dockerfile .
	@docker run --rm -v $(CURDIR)/rpms/RockyLinux10:/root/rpmbuild/RPMS:Z -v $(CURDIR):/workspace:Z localhost/${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG_ROCKY10}
	@docker run --rm -v $(CURDIR):/workspace:Z --entrypoint '' localhost/${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG_ROCKY10} rpm -i /workspace/rpms/RockyLinux10/noarch/*.rpm

rpm-fedora43:
	@docker build -t localhost/${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG_FEDORA43} -f docker/rpm/Fedora43/Dockerfile .
	@docker run --rm -v $(CURDIR)/rpms/Fedora43:/root/rpmbuild/RPMS:Z -v $(CURDIR):/workspace:Z localhost/${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG_FEDORA43}
	@docker run --rm -v $(CURDIR):/workspace:Z --entrypoint '' localhost/${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG_FEDORA43} rpm -i /workspace/rpms/Fedora43/noarch/*.rpm

rpms: rpm-leap16 rpm-tumbleweed rpm-rocky10 rpm-fedora43

clean:
	@rm -rf debs rpms build .pybuild
	@rm -rf debian/cobbler-tftp debian/.debhelper debian/*.debhelper.log debian/*.debhelper debian/*.substvars debian/debhelper-build-stamp debian/files
	@rm -rf src/*.egg-info src/*.dist-info
	@rm -f src/cobbler_tftp/data/version.cfg

.PHONY: rpms rpm-leap16 rpm-tumbleweed rpm-rocky10 rpm-fedora43 deb container-image build clean
