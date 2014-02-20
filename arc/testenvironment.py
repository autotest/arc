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
Module with interface for fetching and manipulating hosts on a autotest server
"""

import re
import functools

import arc.base
import arc.label
import arc.shared.frontend


__all__ = ['get_data',
           'get_ids',
           'get_data_by_id',
           'TestEnvironment']


#
# Service on RPC server hosting these methods
#
SERVICE_NAME = arc.shared.frontend.AFE_SERVICE_NAME


#
# Name of fields as defined on the server side database
#
ID_FIELD = 'id'


#
# Name of RPC methods as defined on the server side
#
GET_METHOD = 'get_test_environments'


#
# Boiler plate code for remote methods that are generic enough to be reused
#
get_data = functools.partial(arc.base.get_data, SERVICE_NAME, GET_METHOD)
get_ids = functools.partial(arc.base.get_and_filter, get_data, ID_FIELD)
get_data_by_id = functools.partial(arc.base.get_by, SERVICE_NAME, GET_METHOD,
                                   ID_FIELD)


class TestEnvironment(arc.base.Model):
    """
    Interface for manipulating hosts on an autotest server
    """
    ID_FIELD = ID_FIELD
    NAME_FIELD = ID_FIELD
    FIELDS = ['distro']
    def __init__(self, connection, identification=None, name=None):
        super(LinuxDistro, self).__init__(connection,
                                          identification,
                                          name)

    def _get_data_by_id(self):
        return get_data_by_id(self.connection, self.identification)

    def _get_data_by_name(self):
        return get_data_by_name(self.connection, self.name)

    def __repr__(self):
        return "<TestEnvironment Name: %s>" % self.name
