#!/usr/bin/bash

pip3 install --break-system-packages -e .
cobbler-tftp start --no-daemon
