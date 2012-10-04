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

Connection to an AFE Service
----------------------------

The class that actually powers the connection return by :func:`arc.connection.get_default` is :class:`arc.connection.AfeConnection`:

.. autoclass:: arc.connection.AfeConnection
   :members: run

You may have noticed that while the utility function :func:`arc.connection.get_default` does not mention the AFE service in its name. That's because, by convention, the default connection is to the AFE service. Actually, the Connection class is an alias to the :class:`arc.connection.AfeConnection`.

.. autoclass:: arc.connection.Connection

Connection to an TKO Service
----------------------------

Last but not least, there's also a TkoConnection object that connects to TKO Service on an autotest server. To use an TkoConnection, instantiate it manually. Currently there's no utility function for it.

.. autoclass:: arc.connection.TkoConnection
   :members: run
