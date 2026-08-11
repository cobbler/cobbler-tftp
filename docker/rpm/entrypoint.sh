#!/bin/bash

echo " ===> Extracting version"
VERSION=$(python3 -m setuptools_scm)
echo "%define version ${VERSION}" >~/rpmbuild/.version

echo " ===> Creating source archive"
base=$(basename "$PWD")
cd ..
tar --exclude "debian/cobbler-tftp" --exclude "debian/.debhelper" --exclude "debs" --exclude "rpms" --exclude ".mypy_cache" --exclude ".idea" --exclude="venv" --exclude "dist" --exclude "build" --transform="s/workspace/cobbler-tftp-${VERSION}/" -zcvf "cobbler-tftp-${VERSION}.tar.gz" /workspace
cd "$base" || exit

echo " ===> Copy required files into build environment"
rm -rf ~/rpmbuild/SOURCES/*
cp "/cobbler-tftp-${VERSION}.tar.gz" ~/rpmbuild/SOURCES/
cp cobbler-tftp.spec ~/rpmbuild/SPECS/
# The spec's "Version: 0" is a placeholder OBS's set_version source service
# rewrites at submission time; do the same rewrite here so Source0's
# %{name}-%{version}.tar.gz matches the tarball actually built above
# (rpmbuild's Version: tag would otherwise override --define version=...).
sed -i "s/^Version:.*/Version:        ${VERSION}/" ~/rpmbuild/SPECS/cobbler-tftp.spec
cd ~/rpmbuild/SOURCES || exit
tar -xzvf "./cobbler-tftp-${VERSION}.tar.gz"
cd "/workspace" || exit

echo " ===> Run rpmbuild inside the container"
rpmbuild --define "_topdir /root/rpmbuild" \
    --define "version ${VERSION}" \
    --bb /root/rpmbuild/SPECS/cobbler-tftp.spec
