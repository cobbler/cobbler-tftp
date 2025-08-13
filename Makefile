DOCKER_IMAGE_NAME=cobbler-tftp-pkg
DOCKER_IMAGE_TAG_OCI=oci
DOCKER_IMAGE_TAG_DEBIAN=debian-13
DOCKER_IMAGE_TAG_OPENSUSE_TW=opensuse-tumbleweed

build:
	@python3 -m setuptools_scm --force-write-version-files
	@python3 -m pip wheel --verbose --use-pep517 --wheel-dir ./build .

container-image:
	@docker build -t localhost/${DOCKER_IMAGE_TAG_OCI} -f docker/production/Dockerfile .

deb:
	@docker build -t localhost/${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG_DEBIAN} -f docker/deb/Debian_13/Dockerfile .
	@docker run --rm -v $(CURDIR)/debs/Debian_13:/usr/src/cobbler-tftp/deb-build -v $(CURDIR):/workspace localhost/${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG_DEBIAN}
	@docker run --rm -v $(CURDIR):/workspace --entrypoint '' localhost/${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG_DEBIAN} bash -c 'dpkg -i /workspace/debs/Debian_13/cobbler-tftp*.deb'

rpm:
	@docker build -t localhost/${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG_OPENSUSE_TW} -f docker/rpm/openSUSE_tumbleweed/Dockerfile .
	@docker run --rm -v $(CURDIR)/rpms/openSUSE_tumbleweed:/root/rpmbuild/RPMS -v $(CURDIR):/workspace localhost/${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG_OPENSUSE_TW}
	@docker run --rm -v $(CURDIR):/workspace --entrypoint '' localhost/${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG_OPENSUSE_TW} rpm -i /workspace/rpms/openSUSE_tumbleweed/noarch/*.rpm

clean:
	@rm -rf debs rpms build .pybuild
	@rm -rf debian/cobbler-tftp debian/.debhelper debian/*.debhelper.log debian/*.debhelper debian/*.substvars debian/debhelper-build-stamp debian/files
	@rm -rf src/*.egg-info src/*.dist-info
	@rm -f src/cobbler_tftp/data/version.cfg

.PHONY: rpm deb container-image build clean
