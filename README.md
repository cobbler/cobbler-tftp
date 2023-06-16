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

## Installation (WIP)

Please note that Cobbler-TFTP is currently still in an early development stage and is not yet ready to be released.
However, these methods of Installation will be available:

### Installation Requirements

To install and use Cobbler-TFTP, please make sure you have *at least Python 3.6* installed.

### Install via `pip`

Cobbler-TFTP is published to PyPi.
To install it, please make sure that your system fulfills the installation requirements listed above and has `pip`,
the Python package manager, installed.

To install Cobbler-TFTP you can then simply run:
```bash
pip install cobbler-tftp
```

### Install on Linux via Package manager

Cobbler-TFTP is packaged for a number of Linux distributions.

Note: The native linux packages do not yet exist.
These instructions are just representing what we have planned for the near future.

#### Install on openSUSE

```bash
sudo zypper install cobbler-tftp
```

#### Install on Fedora

```bash
sudo dnf install cobbler-tftp
```

#### Install on Debian, Ubuntu and Linux Mint

```bash
sudo apt install cobbler-tftp
```

<!-- ### Install as container from Docker Hub -->

## Usage

You can use Cobbler-TFTP out of the box when providing it your Cobbler API credentials.

You can do so with a `settings.yml`configuration file, environment variables and/or command line flags.

To run Cobbler-TFTP simply run:

```bash
cobbler-tftp
```

### Configuring Cobbler-TFTP

The default parameters for Cobbler-TFTP's application settings will be taken, if no configuration file,
command line argument or environment variable can be found, will be as follows:

```yaml
schema: 1.0 # The version of the configuration schema to use
auto_migrate_settings: false # Automatically migrate to the newest configuration schema
is_daemon: true # Run Cobbler-TFTP as a daemon
cobbler:
  uri: "http://localhost/cobbler_api" # uri of your Cobbler API
  username: "cobbler" # Username for Cobbler
  password: "cobbler"
  password_file: "/etc/cobbler-tftp/cobbler_password" # File containing your Cobbler password.
```

**Please note** that the `password` and `password_file` settings are mutually exclusive.
Custom configuration files containing both parameters will not be accepted.

#### Using a configuration yaml file

Cobbler-TFTP can be configured using a custom `settings.yml` file.
Note, that this file must contain at least all parameters listed above.

To pass the file on you can pass the file location on as a CLI argument using the `-c` or `--config` flag:

```bash
cobbler-tftp -c path/to/your/file.yml
```

#### Using environment variables

You can set certain parameters of Cobbler-TFTP's behavior by using environment variables.
These will override the configuration from your configuration file.

Cobbler-TFTP will automatically search for environment variables in this format:

```
COBBLER_TFTP__<PARENT_KEY>__<CHILD_KEY>__<...>__<KEY>=<VALUE>
```

For example your variables might look like this:

```
COBBLER_TFTP__IS_DAEMON=true
```

or, in case of your Cobbler settings:

```
COBBLER_TFTP__COBBLER__URI=http://your.domain.com/cobbler_api
```

#### Using CLI arguments

You can also provide Cobbler-TFTP with CLI arguments to override some or all of the above parameters.

These must be given in the format:

```
<PARENT_KEY>.<CHILD_KEY>.<...>.<KEY>=<VALUE>
```

These arguments will override all of the parameters above and will be lost when the service is stopped and restarted.

We advise you to use this option for testing purposes only.

## Documentation

You can find our latest documentation on our [Read the Docs Page](https://cobbler-tftp.readthedocs.io/en/latest/)

## Contributing

If you would like to contribute to this project, you can take a look at our [contributing guide](./CONTRIBUTING.md)
for a detailed guide on how you can help to make Cobbler-TFTP the best int can be.

We greatly appreciate any contribution!
