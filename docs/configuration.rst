************************
Configuring Cobbler-TFTP
************************

Cobbler-TFTP can be configured in several different ways.

Configuration via a config-File
===============================

Configuring Cobbler-TFTP by using a configuration .yaml-File is the recommended way.
Using a ``settings.yaml`` allows you to set up a persistent configuration of the Cobbler-TFTP server.

An example file looks like this:

.. code-block:: yaml

   schema: 1.0 # The version of the configuration schema to use
   auto_migrate_settings: false # Automatically migrate to the newest configuration schema
   is_daemon: true # Run Cobbler-TFTP as a daemon
   cobbler:
      uri: "http://localhost/cobbler_api" # uri of your Cobbler API
      username: "cobbler" # Username for Cobbler
      password: "cobbler"
      password_file: "/etc/cobbler-tftp/cobbler_password" # File containing your Cobbler password.

This configuration is also the *default* configuration of Cobbler-TFTP, which is used if no other
configuration parameters can be found from other sources.

To pass the file to Cobbler-TFTP, you can pass the file location as a CLI argument using the ``-c`` or
``--config`` flag.

.. code-block:: bash

   cobbler-tftp -c path/to/your/settings.yml

Configuration via environment variables
=======================================

You can set certain parameters of Cobbler-TFTP's behaviour by using environment variables.
These **will override the configuration from your configuration file**.

Cobbler-TFTP will automatically search for environment variables in this format:

.. code-block:: bash

   COBBLER_TFTP__<PARENT_KEY>__<CHILD_KEY>__<...>__<KEY>=<VALUE>

For example your variables might look like this:

.. code-block:: bash

   COBBLER_TFTP__IS_DAEMON=true

or, in case of your Cobbler settings:

.. code-block:: bash

   COBBLER_TFTP__COBBLER__URI=http//your.domain.com/cobbler_api

Configuration via CLI parameters
================================

Youc an also provide Cobbler-TFTP with CLI arguments to **override some or all** of the above
parameters.

These must be given in the format:

.. code-block:: bash

   <PARENT_KEY>.<CHILD_KEY>.<..>.<KEY>=<VALUE>

These arguments will override values from **all other sources** and will be lost
when the service is stopped and restarted.

We advise you to use this option for testing purposes only.
