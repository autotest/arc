.. _arc-api-label:

:mod:`label` --- Manipulating machines that run tests
=====================================================

Labels are how Autotest attaches information to :class:`Host`.

The functionality exposed by the server allow users to add new labels,
modify and delete existing ones. Also you can add or remove labels to
existing hosts.

Functions for procedural like programming
-----------------------------------------

All the default functions are available for getting information, adding new instances, modifying and deleting existing ones.

.. function:: arc.label.get_data

   |get_data|

   :param connection: an :class:`arc.connection.AfeConnection` instance
   :param data_filter: keyword arguments to filter the data that will be received
   :return: raw JSON data converted to a Python data structure

.. function:: arc.label.get_ids

   Returns only the numeric identification of existing instances on the server side.

   :param connection: an :class:`arc.connection.AfeConnection` instance
   :param data_filter: keyword arguments to filter the data that will be received
   :return: raw JSON data converted to a Python data structure


The Label Class
---------------

.. autoclass:: arc.label.Label
   :members:

.. include:: defs.txt
