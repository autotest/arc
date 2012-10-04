.. _arc-api-host:

:mod:`host` --- Manipulating machines that run tests
====================================================

Hosts are the Autotest terminology for machines that will run the test jobs.

The functionality exposed by the server allow users to add new hosts,
modify or delete existing ones.

As an implementation detail of the server, to maintain referential integrity,
a host record is never actually deleted, but marked as invalid.

Functions for procedural like programming
-----------------------------------------

All the default functions are available for getting information, adding new instances, modifying and deleting existing ones.

.. function:: arc.host.get_data

   |get_data|

   :param connection: an :class:`arc.connection.AfeConnection` instance
   :param data_filter: keyword arguments to filter the data that will be received
   :return: raw JSON data converted to a Python data structure

.. function:: arc.host.get_ids

   Returns only the numeric identification of existing instances on the server side.

   :param connection: an :class:`arc.connection.AfeConnection` instance
   :param data_filter: keyword arguments to filter the data that will be received
   :return: raw JSON data converted to a Python data structure


The Host Class
--------------

.. autoclass:: arc.host.Host
   :members:

.. include:: defs.txt
