#!/usr/bin/bash

git config --global --add safe.directory /code
python3 -m venv /venv
source /venv/bin/activate
python3 -m pip install -e .
cobbler-tftp start --no-daemon
