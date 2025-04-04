deb:
	@docker build -t localhost/cobbler-tftp-pkg:debian-12 -f docker/deb/Debian_12/Dockerfile .
	@docker run --rm -v $(CURDIR)/debs/Debian_12:/usr/src/cobbler-tftp/deb-build -v $(CURDIR):/workspace localhost/cobbler-tftp-pkg:debian-12

rpm:
	@docker build -t localhost/cobbler-tftp-pkg:opensuse-tumblewed -f docker/rpm/openSUSE_tumbleweed/Dockerfile .
	@docker run --rm -v $(CURDIR)/rpms/openSUSE_tumbleweed:/root/rpmbuild/RPMS -v $(CURDIR):/workspace localhost/cobbler-tftp-pkg:opensuse-tumblewed

.PHONY: rpm deb