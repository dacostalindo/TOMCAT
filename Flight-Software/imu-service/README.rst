IMU Service
===================



Examples
--------

Example query:

.. code::

  query {
    imu-Telemetry(
      module:"sim",
      fields:["firmware_version","commands_parsed","scpi_errors"]
    )
  }


Some commands to run to test from the command line (for module "sim"):

.. code::

  echo "query {moduleList}" | nc -uw1 127.0.0.1 8150
  echo "query {fieldList(module:\"sim\")}" | nc -uw1 127.0.0.1 8150
  echo "mutation {passthrough(module:\"sim\",command:\"SUP:LED ON\"){status,command}}" | nc -uw1 127.0.0.1 8150

Testing
-------

In the tests folder, there is an integration test script that can be run to verify communication with all modules on the bus. It will retrieve what modules are present, request what fields are available for each module, and retrieve all available telemetry for each module.

Run with:

.. code::

  python integration_test.py -c /path/to/service/config.toml
