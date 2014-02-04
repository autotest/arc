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
# Copyright (c) 2014 Red Hat
# Author: Ruda Moura <rmoura@redhat.com>

"""
Module with interface for fetching and manipulating ACL
groups on a autotest server.
"""

import functools

import arc.base
import arc.defaults
import arc.shared.frontend


__all__ = ['get_data',
           'get_ids',
           'get_names',
           'get_ids_names',
           'get_data_by_id',
           'get_data_by_name',
           'add',
           'delete',
           'modify',
           'AclGroup',
           'get_objs']


#
# Service on RPC server hosting these methods
#
SERVICE_NAME = arc.shared.frontend.AFE_SERVICE_NAME


#
# Name of fields as defined on the server side database
#
ID_FIELD = 'id'
NAME_FIELD = 'name'


#
# Name of RPC methods as defined on the server side
#
GET_METHOD = 'get_acl_groups'
ADD_METHOD = 'add_acl_group'
DELETE_METHOD = 'delete_acl_group'
MODIFY_METHOD = 'modify_acl_group'


#
# Boiler plate code for remote methods that are generic enough to be reused
#
get_data = functools.partial(arc.base.get_data, SERVICE_NAME, GET_METHOD)
get_ids = functools.partial(arc.base.get_and_filter, get_data, ID_FIELD)
get_names = functools.partial(arc.base.get_and_filter, get_data, NAME_FIELD)
get_ids_names = functools.partial(arc.base.get_id_name_and_filter, get_data,
                                  ID_FIELD, NAME_FIELD)
get_data_by_id = functools.partial(arc.base.get_by, SERVICE_NAME, GET_METHOD,
                                   ID_FIELD)
get_data_by_name = functools.partial(arc.base.get_by, SERVICE_NAME, GET_METHOD,
                                     NAME_FIELD)
delete = functools.partial(arc.base.delete, SERVICE_NAME, DELETE_METHOD)


#
# Methods that have add more logic related to the manipulated object nature
#
def add(connection, name, description=None):
    """
    Add a new acl_group entry
    """
    return connection.run(SERVICE_NAME, ADD_METHOD, name, description)


class AclGroup(arc.base.Model):
    """
    Interface for manipulating ACL groups on an autotest server
    """
    ID_FIELD = ID_FIELD
    NAME_FIELD = NAME_FIELD
    FIELDS = ['description', 'users', 'hosts']

    def __init__(self, connection, identification=None, name=None):
        super(AclGroup, self).__init__(connection, identification, name)

    def _get_data_by_id(self):
        return get_data_by_id(self.connection, self.identification)

    def _get_data_by_name(self):
        return get_data_by_name(self.connection, self.name)


get_objs = functools.partial(arc.base.get_objs, get_ids_names, AclGroup)
