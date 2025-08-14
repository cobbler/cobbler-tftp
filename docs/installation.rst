***********************
Installing Cobbler-TFTP
***********************

Please note that Cobbler-TFTP is currently still in an early development stage and is not yet ready to be released.
However, these methods of Installation will be available:

Installation Requirements
=========================

To install and use Cobbler-TFTP, please make sure you have *at least Python 3.8* installed.

Install via `pip`
=================

Cobbler-TFTP is published to PyPi.
To install it, please make sure that your system fulfills the installation requirements listed above and has `pip`,
the Python package manager, installed.

To install Cobbler-TFTP you can then simply run:

.. code-block:: bash

   pip install cobbler-tftp


Install on Linux via Package manager
====================================

Cobbler-TFTP is packaged for a number of Linux distributions.

Note: The native linux packages do not yet exist.
These instructions are just representing what we have planned for the near future.

Install on openSUSE
-------------------

.. code-block:: bash

   sudo zypper install cobbler-tftp

Install on Fedora
-----------------

.. code-block:: bash

   sudo dnf install cobbler-tftp


Install on Debian, Ubuntu and Linux Mint
----------------------------------------

.. code-block:: bash

   sudo apt install cobbler-tftp
