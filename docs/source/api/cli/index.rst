.. _arc-api-cli:

CLI
===

The main arc command line application is called arcli and all of its logic is implemented by modules on the arc.cli namespace. The arcli script itself is just a thin wrapper that initializes arc.cli.app.App.

Arc is designed like that so that users can build their own custom applications with minimal effort.

.. toctree::
   :maxdepth: 1

   app
   actions
