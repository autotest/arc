# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
# See LICENSE for more details.
#
# Copyright (c) 2013-2014 Red Hat
# Author: Cleber Rosa <cleber@redhat.com>

"""
This module holds a collection of data that is set as the default value
for a number of items that control the behavior of both the API and
the CLI tool.

For API users, when a given function or method is not called with and
explicit value (usually having a parameter that at the function call
level defaults to 'None'), these values are automatically used.

For the CLI tool, these values are set as defaults when an explicit value
is not provided either on the configuration file or on the command line.
"""

#: The global, system wide configuration file path
CONFIG_SYS_PATH = '/etc/arc.conf'
#: The local, user owned configuration file path
CONFIG_USR_PATH = '~/.arc.conf'

#: The default host to connect to
SERVER_HOST = 'localhost'
#: The default port to connect to
SERVER_PORT = 80

#: Python namespace prefix for CLI arguments
ARGS_MODULE_PREFIX = 'arc.cli.args'
#: Python namespace prefix for CLI actions
ACTIONS_MODULE_PREFIX = 'arc.cli.actions'
