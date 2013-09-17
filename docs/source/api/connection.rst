.. _arc-api-connection:

:mod:`connection` --- Connecting to an Autotest RPC Server
==========================================================

The :mod:`connection` module provides the means to actually talk to the services hosted on an Autotest Server.

Default Connection
------------------

Most users of the connection module will only be interested in the AFE service, and also will only be interested in getting a connection to it that is:

 * Ready to use
 * Global
 * Respect default settings

For those users, the :func:`arc.connection.get_default` does just that:

.. autofunction:: arc.connection.get_default

BaseConnection
--------------

.. autoclass:: arc.connection.BaseConnection
   :members:


Connection
----------

This is the class that actually powers the connection return by :func:`arc.connection.get_default`.

.. autoclass:: arc.connection.Connection
   :members:

By default, instances of this classes register access to both the AFE and TKO serviceces (by means of running :meth:`arc.connection.BaseConnection.add_service`).
