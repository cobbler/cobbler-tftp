#!/bin/bash

echo " ===> Extracting version"
VERSION=$(python3 -m setuptools_scm)
echo "%define version ${VERSION}" > ~/rpmbuild/.version

echo " ===> Creating source archive"
base=$(basename "$PWD")
cd ..
tar --exclude ".idea" --exclude="venv" --exclude "dist" --exclude "build" --transform="s/workspace/cobbler-tftp-${VERSION}/" -zcvf "cobbler-tftp-${VERSION}.tar.gz" /workspace
cd "$base" || exit

echo " ===> Copy required files into build environment"
rm -rf ~/rpmbuild/SOURCES/*
cp "/cobbler-tftp-${VERSION}.tar.gz" ~/rpmbuild/SOURCES/
cp cobbler-tftp.spec ~/rpmbuild/SPECS/
cd ~/rpmbuild/SOURCES || exit
tar -xzvf "./cobbler-tftp-${VERSION}.tar.gz"
cd "/workspace" || exit

echo " ===> Run rpmbuild inside the container"
rpmbuild --define "_topdir /root/rpmbuild" \
    --define "version ${VERSION}" \
    --bb /root/rpmbuild/SPECS/cobbler-tftp.spec
