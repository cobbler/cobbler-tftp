build:
	@python3 -m setuptools_scm --force-write-version-files
	@python3 -m pip wheel --verbose --use-pep517 --wheel-dir ./build .

deb:
	@docker build -t localhost/cobbler-tftp-pkg:debian-13 -f docker/deb/Debian_13/Dockerfile .
	@docker run --rm -v $(CURDIR)/debs/Debian_13:/usr/src/cobbler-tftp/deb-build -v $(CURDIR):/workspace localhost/cobbler-tftp-pkg:debian-13

rpm:
	@docker build -t localhost/cobbler-tftp-pkg:opensuse-tumblewed -f docker/rpm/openSUSE_tumbleweed/Dockerfile .
	@docker run --rm -v $(CURDIR)/rpms/openSUSE_tumbleweed:/root/rpmbuild/RPMS -v $(CURDIR):/workspace localhost/cobbler-tftp-pkg:opensuse-tumblewed

clean:
	@rm -rf debs rpms build .pybuild
	@rm -rf debian/cobbler-tftp debian/.debhelper debian/*.debhelper.log debian/*.debhelper debian/*.substvars debian/debhelper-build-stamp debian/files
	@rm -rf src/*.egg-info src/*.dist-info
	@rm -f src/cobbler_tftp/data/version.cfg

.PHONY: rpm deb build clean
