#!/bin/bash

DEB_BUILD_OPTIONS="nocheck" debuild -us -uc
cp ../cobbler-tftp_* /usr/src/cobbler-tftp/deb-build
