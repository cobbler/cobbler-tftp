rpm:
	@docker build -t localhost/cobbler-tftp-pkg:opensuse-tumblewed -f docker/rpm/openSUSE_tumbleweed/Dockerfile .
	@docker run --rm -v $(CURDIR)/rpms/openSUSE_tumbleweed:/root/rpmbuild/RPMS -v $(CURDIR):/workspace localhost/cobbler-tftp-pkg:opensuse-tumblewed

.PHONY: rpm