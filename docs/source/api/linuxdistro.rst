.. _arc-api-host:

:mod:`linuxdistro` --- Manipulating known Linux Distributions
=============================================================

Autotest can have knowledge about the Linux Distribution that was running on
a machine during a test their detailed charateristics.

Functions for procedural like programming
-----------------------------------------

All the default functions are available for getting information.

.. function:: arc.linuxdistro.get_data

   |get_data|

   :param connection: an :class:`arc.connection.Connection` instance
   :param data_filter: keyword arguments to filter the data that will be received
   :return: raw JSON data converted to a Python data structure

.. function:: arc.linuxdistro.get_ids

   Returns only the numeric identification of existing instances on the server side.

   :param connection: an :class:`arc.connection.Connection` instance
   :param data_filter: keyword arguments to filter the data that will be received
   :return: raw JSON data converted to a Python data structure


The Host Class
--------------

.. autoclass:: arc.linuxdistro.LinuxDistro
   :members:

.. include:: defs.txt
