"""
Configuration file parser

This class provides a parser for the client side configuration file, both the
system wide client configuration, and the local user configuration file.

The local user configuration file overrides values that may be set in the
system wide configuration file.
"""


import os

import arc.defaults


__all__ = ['get_default',
           'SystemWideConfigParser',
           'UserLocalConfigParser',
           'Config']


try:
    import ConfigParser as configparser
except ImportError:
    import configparser


class SystemWideConfigParser(configparser.ConfigParser):
    """
    This is a parser for the system wide configuration for the autotest rpc
    client library.
    """
    DEFAULT_PATH = arc.defaults.CONFIG_SYS_PATH


    def __init__(self):
        configparser.ConfigParser.__init__(self)

        if os.path.exists(self.DEFAULT_PATH):
            self.read(self.DEFAULT_PATH)


class UserLocalConfigParser(configparser.ConfigParser):
    """
    This is a parser for the configuration file that is specific to the
    current user and lives on his home directory.

    If the system wide configuration exists, it is also read, though
    the values in the user specific configuration file overrides the
    previous one.
    """
    DEFAULT_PATH = os.path.expanduser(arc.defaults.CONFIG_USR_PATH)


    def __init__(self):
        configparser.ConfigParser.__init__(self)

        paths = []
        if os.path.exists(SystemWideConfigParser.DEFAULT_PATH):
            paths.append(SystemWideConfigParser.DEFAULT_PATH)
        paths.append(self.DEFAULT_PATH)

        self.read(paths)


    def get_server_host(self):
        """
        Returns the server host, defaulting to what is in :mod:`arc.defaults`
        """
        section = 'server'
        key = 'host'
        value = None
        if self.has_section(section):
            value = self.get(section, key)
        if not value:
            value = arc.defaults.SERVER_HOST

        return value


Config = UserLocalConfigParser
CONFIG = None


def get_default(klass=Config):
    """
    Returns the default configuration

    :param klass: a Configurtion class to be instantiated one time only.
           Defaults to :class:`UserLocalConfigParser`
    """
    global CONFIG

    if CONFIG is None:
        CONFIG = klass()

    return CONFIG
