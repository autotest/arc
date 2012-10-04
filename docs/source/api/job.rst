.. _arc-api-job:

:mod:`job` --- Manipulating test jobs
=====================================

Jobs are the Autotest terminology for test that is either scheduled to be executed, is running, or has already finished runnning.

Functions for procedural like programming
-----------------------------------------

All the default functions are available for getting information, adding new instances, modifying and deleting existing ones.

.. function:: arc.job.get_data

   |get_data|

   :param connection: an :class:`arc.connection.AfeConnection` instance
   :param data_filter: keyword arguments to filter the data that will be received
   :return: raw JSON data converted to a Python data structure

.. function:: arc.job.get_ids

   Returns only the numeric identification of existing instances on the server side.

   :param connection: an :class:`arc.connection.AfeConnection` instance
   :param data_filter: keyword arguments to filter the data that will be received
   :return: raw JSON data converted to a Python data structure


The Job Class
-------------

.. autoclass:: arc.job.Job
   :members:

.. include:: defs.txt
