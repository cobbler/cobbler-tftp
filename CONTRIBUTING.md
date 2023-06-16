# Contributing

Thank you for your interest in contributing to Cobbler-TFTP.<br>
This guide will show you how to set up your development environment.


## Getting started

To get started first you need to
[fork this repository](https://docs.github.com/en/get-started/quickstart/fork-a-repo),
so you have your very own copy of the Cobbler-TFTP source code in you own GitHub profile.

After this is done,
[clone your fork](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository)
clone your fork to a directory of your choosing and change to that directory.

Once in there you can add the original repository as a git remote so you can pull the latest changes without extra
steps.

You can do so like this:

```bash
git remote add upstream git@github.com:cobbler/cobbler-tftp.git
```

After this step, you can simply pull the latest changes of Cobbler-TFTP with `git pull upstream main`.

## Setting up the environment

After you have cloned the source code you need to set up a virtual environment using either
[virtualenv](https://virtualenv.pypa.io/en/latest/) or [pyenv](https://github.com/pyenv/pyenv) to make sure your
system does not affect the integrity of your changes.

When this is completed, you then need to install all requirements.<br>
You can do so by running this command:

```bash
pip install -e .[tests_require,lint_requires,doc]
```
Pip will then install Cobbler-TFTP alongside all of the additional dependencies required for contributing.

Now you can start making changes to Cobbler-TFTP!