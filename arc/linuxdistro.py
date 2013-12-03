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
           'get_names',
           'get_ids_names',
           'get_data_by_id',
           'get_data_by_name',
           'LinuxDistro',
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
GET_METHOD = 'get_linux_distros'


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


class LinuxDistro(arc.base.Model):
    """
    Interface for manipulating hosts on an autotest server
    """
    ID_FIELD = ID_FIELD
    NAME_FIELD = NAME_FIELD
    FIELDS = ['version', 'release', 'arch']

    def __init__(self, connection, identification=None, name=None):
        super(LinuxDistro, self).__init__(connection,
                                          identification,
                                          name)

    def _get_data_by_id(self):
        return get_data_by_id(self.connection, self.identification)

    def _get_data_by_name(self):
        return get_data_by_name(self.connection, self.name)

    def __repr__(self):
        return "<LinuxDistro Name: %s>" % self.name


get_objs = functools.partial(arc.base.get_objs,
                             get_ids_names,
                             LinuxDistro)
