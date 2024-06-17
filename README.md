# Cobbler-TFTP

[![Codacy Badge](https://app.codacy.com/project/badge/Grade/97c9e642afd646e98b9250e2959aae12)](https://app.codacy.com/gh/cobbler/cobbler-tftp/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)
[![Codacy Badge](https://app.codacy.com/project/badge/Coverage/97c9e642afd646e98b9250e2959aae12)](https://app.codacy.com/gh/cobbler/cobbler-tftp/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_coverage)
[![Tests](https://github.com/cobbler/cobbler-tftp/actions/workflows/testing.yml/badge.svg)](https://github.com/cobbler/cobbler-tftp/actions/workflows/testing.yml)
[![Documentation Status](https://readthedocs.org/projects/cobbler-tftp/badge/?version=latest)](https://cobbler-tftp.readthedocs.io/en/latest/?badge=latest)

[![Matrix](https://img.shields.io/matrix/cobbler-community:matrix.org?label=Chat%20on%20Matrix&logo=matrix)](https://app.element.io/#/room/#cobbler_community:gitter.im)

---

Cobbler-TFTP is a lightweight CLI application written in Python that serves as a stateless TFTP server.
It seamlessly integrates with Cobbler to generate and serve boot configuration files dynamically to managed machines.


## Features

- Stateless TFTP server for network booting and provisioning
- Interoperates with Cobbler for centralized management and configuration deployment
- Dynamic on-demand generation of boot configuration files for efficient resource use
- Configurable daemon process

## Quickstart

Please note that Cobbler-TFTP is currently still in an early development stage and is not yet ready to be released.

To get started quickly with `cobbler-tftp`, simply install it using `pip` and start the daemon.

```bash
pip install cobbler-tftp && cobbler-tftp
```

For a more in-depth guide on how to use and configure `cobbler-tftp` - as well as additional
installation options - please refer to our [documentation](https://cobbler-tftp.readthedocs.io/en/latest/).

## Documentation

You can find our latest documentation on our [Read the Docs Page](https://cobbler-tftp.readthedocs.io/en/latest/).

## Contributing

If you would like to contribute to this project, you can take a look at our [contributing guide](./CONTRIBUTING.md)
for a detailed guide on how you can help to make Cobbler-TFTP the best int can be.

We greatly appreciate any contribution!
