"""
This module provides connection classes to both the AFE and TKO services of the
autotest server.

A connection is a simple wrapper around a JSON-RPC Proxy instance. It is the
basic object that allows methods to be called on the remote RPC server.
"""


__all__ = ['get_default', 'Connection', 'AfeConnection', 'TkoConnection']


import os

import arc.config
import arc.defaults
import arc.jsonrpc


class AuthError(Exception):
    """
    Authentication Error reported users of the connection module
    """
    pass


class RpcAuthError(Exception):
    """
    Internal (between connection and Rpc Proxy) Authentication Error
    """
    pass


class BaseConnection(object):
    """
    Base RPC connection
    """
    def __init__(self, hostname=None, path=None):
        """
        Initializes a connection to an empty path

        This empty path does not exist on a default Autotest server
        """
        if hostname is None:
            hostname = arc.config.get_default().get_server_host()
        self.hostname = hostname

        if path is None:
            path = arc.defaults.RPC_PATH

        try:
            self.proxy = self._connect(path)
        except RpcAuthError:
            raise AuthError


    def _connect(self, path):
        """
        Setup authorization headers and instantiate a JSON RPC Service Proxy

        :param path: the URI path where the service is hosted
        """
        headers = {'AUTHORIZATION': os.environ.get('USER', 'debug_user')}
        rpc_uri = "http://%s%s" % (self.hostname, path)
        return arc.jsonrpc.ServiceProxy(rpc_uri, headers=headers)


    def run(self, operation, *args, **data):
        """
        Runs a method using the rpc proxy

        This method is heavily used by upper level API methods, and more often
        than not, those upper level API methods should be used instead.

        :param operation: the name of the RPC method on the Autotest server
        :param args: positional arguments to be passed to the RPC method
        :param data: keyword arguments to be passed to the RPC method
        """
        function = getattr(self.proxy, operation)
        result = function(*args, **data)
        return result


    def ping(self):
        """
        Tests connectivity to the RPC server
        """
        result = self.run("ping")
        return result == True


class AfeConnection(BaseConnection):
    """
    A connection to the AFE service

    :param hostname: the IP address or hostname of the server that will be
           contacted upon RPC method execution.
    :param path: the base URI where the server is running the AFE service
    """
    def __init__(self, hostname=None, path=arc.defaults.AFE_RPC_PATH):
        super(AfeConnection, self).__init__(hostname, path)


#: Connection is an alias to AfeConnection, since it's the most used service
Connection = AfeConnection


class TkoConnection(BaseConnection):
    """
    A connection to the TKO service

    :param hostname: the IP address or hostname of the server that will be
           contacted upon RPC method execution.
    :param path: the base URI where the server is running the TKO service

    """
    def __init__(self, hostname=None, path=arc.defaults.TKO_RPC_PATH):
        super(TkoConnection, self).__init__(hostname, path)


#: Global, default connection to an AFE service for ease of use by apps
AFE_CONNECTION = None


def get_default():
    """
    Returns the global, default connection to an AFE service

    :returns: an arc.connection.AfeConnection instance
    """
    global AFE_CONNECTION

    if AFE_CONNECTION is None:
        AFE_CONNECTION = AfeConnection()

    return AFE_CONNECTION
