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
The atomicgroup module contains the objects and methods used to
manage atomic groups in Autotest.
"""

import functools

import arc.base
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
           'add_labels',
           'delete_labels',
           'AtomicGroup',
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
GET_METHOD = 'get_atomic_groups'
ADD_METHOD = 'add_atomic_group'
DELETE_METHOD = 'delete_atomic_group'
MODIFY_METHOD = 'modify_atomic_group'


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
def add(connection, name, description=None, max_number_of_machines=None,
        invalid=None):
    """
    Add a new atomic group entry
    """
    return connection.run(SERVICE_NAME, ADD_METHOD, name, description,
                          max_number_of_machines)


def add_labels(connection, identification, labels):
    """Add labels to an atomic group."""
    return connection.run(SERVICE_NAME, 'atomic_group_add_labels',
                          identification, labels)


def delete_labels(connection, identification, labels):
    """Delete labels from an atomic group."""
    return connection.run(SERVICE_NAME, 'atomic_group_remove_labels',
                          identification, labels)


def modify(connection, identification, **data):
    """
    Modify an atomic group entry

    :param connection:
    :param identification:
    :param data:
    """
    return connection.run(SERVICE_NAME, MODIFY_METHOD, identification, **data)


class AtomicGroup(arc.base.Model):

    """Interface model for Atomic Group on Autotest server."""
    ID_FIELD = ID_FIELD
    NAME_FIELD = NAME_FIELD
    FIELDS = ['description', 'max_number_of_machines', 'invalid']

    def __init__(self, connection, identification=None, name=None):
        super(AtomicGroup, self).__init__(connection, identification, name)

    def _get_data_by_id(self):
        return get_data_by_id(self.connection, self.identification)

    def _get_data_by_name(self):
        return get_data_by_name(self.connection, self.name)


get_objs = functools.partial(arc.base.get_objs, get_ids_names, AtomicGroup)
