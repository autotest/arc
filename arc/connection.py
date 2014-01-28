"""
This module provides connection classes to both the AFE and TKO services of the
autotest server.

A connection is a simple wrapper around a JSON-RPC Proxy instance. It is the
basic object that allows methods to be called on the remote RPC server.
"""

import os

import arc.config
import arc.defaults
import arc.proxy
import arc.shared.frontend
import arc.shared.rpc


__all__ = ['get_default', 'Connection']


#: Minimum required version of server side API
MIN_REQUIRED_VERSION = {}
MIN_REQUIRED_VERSION[arc.shared.frontend.AFE_SERVICE_NAME] = (2013, 9, 11)
MIN_REQUIRED_VERSION[arc.shared.frontend.TKO_SERVICE_NAME] = (2013, 5, 23)


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


class InvalidProxyError(Exception):
    """
    Invalid proxy for selected service
    """
    pass


class InvalidServiceVersionError(Exception):
    """
    The service version does not satisfy the minimum required version
    """
    pass


class BaseConnection(object):
    """
    Base RPC connection
    """
    def __init__(self, hostname=None, port=None, path=None, username=None):
        """
        Initializes a connection to an empty path

        This empty path does not exist on a default Autotest server
        """
        if hostname is None:
            hostname = arc.config.get_default().get_server_host()
        self.hostname = hostname

        if port is None:
            port = arc.config.get_default().get_server_port()
        self.port = port

        if path is None:
            path = arc.shared.rpc.DEFAULT_PATH

        if username is None:
            username = arc.config.get_default().get_username()
        self.username = username

        self.services = {}
        self.service_proxies = {}
        self.service_interface_versions = {}

        try:
            self.proxy = self._connect(path, self.username)
        except RpcAuthError:
            raise AuthError

    def _connect(self, path, username):
        """
        Setup authorization headers and instantiate a JSON RPC Service Proxy

        :param path: the URI path where the service is hosted
        :param username: the username to login
        """
        rpc_uri = "http://%s:%s/%s" % (self.hostname, self.port, path)
        headers = {'AUTHORIZATION': username}
        return arc.proxy.Proxy(rpc_uri, headers)

    def run(self, service, operation, *args, **data):
        """
        Runs a method using the rpc proxy

        This method is heavily used by upper level API methods, and more often
        than not, those upper level API methods should be used instead.

        :param operation: the name of the RPC method on the Autotest server
        :param args: positional arguments to be passed to the RPC method
        :param data: keyword arguments to be passed to the RPC method
        """
        proxy = self.service_proxies.get(service, None)
        if proxy is None:
            raise InvalidProxyError

        function = getattr(proxy, operation)
        result = function(*args, **data)
        return result

    def add_service(self, name, path):
        """
        Add a service to a connection

        :param name: a descriptive name to the service
        :param path: the path in the URI that hosts the service
        """
        self.services[name] = path
        self.service_proxies[name] = self._connect(path, self.username)
        try:
            api_version = tuple(self.run(name, "get_interface_version"))
        except:
            api_version = None
        self.service_interface_versions[name] = api_version

        if not self.check_min_rpc_interface_version(name):
            raise InvalidServiceVersionError

    def check_min_rpc_interface_version(self, service_name):
        """
        Checks the minimum required RPC interface version

        :param service_name: the registered name of the service
        """
        min_version = MIN_REQUIRED_VERSION.get(service_name, None)
        if min_version is None:
            return True

        current_version = self.service_interface_versions.get(service_name,
                                                              None)
        if current_version is None:
            return True

        return current_version >= min_version

    def ping(self):
        """
        Tests connectivity to the RPC server
        """
        try:
            result = self.run(arc.shared.frontend.AFE_SERVICE_NAME,
                              "get_server_time")
        except:
            return False
        return True


class Connection(BaseConnection):
    """
    The default connection that allows access to both AFE and TKO services

    :param hostname: the IP address or hostname of the server that will be
           contacted upon RPC method execution.
    :param port: the port number where the RPC server is running
    """
    def __init__(self, hostname=None, port=None, username=None):
        super(Connection, self).__init__(hostname, port, username=username)
        for (name, path) in arc.shared.rpc.PATHS.items():
            self.add_service(name, path)


#: Global, default connection to an AFE service for ease of use by apps
CONNECTION = None


def get_default():
    """
    Returns the global, default connection to an AFE service

    :returns: an arc.connection.Connection instance
    """
    global CONNECTION

    if CONNECTION is None:
        CONNECTION = Connection()

    return CONNECTION
