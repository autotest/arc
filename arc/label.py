"""
Module with interface for fetching and manipulating labels on a autotest server
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
           'Label',
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
GET_METHOD = 'get_labels'
ADD_METHOD = 'add_label'
DELETE_METHOD = 'delete_label'
MODIFY_METHOD = 'modify_label'


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
def add(connection, name, kernel_config=None, platform=None,
        only_if_needed=None):
    """
    Add a new label entry
    """
    return connection.run(SERVICE_NAME, ADD_METHOD, name, kernel_config,
                          platform, only_if_needed)


class Label(arc.base.Model):
    """
    Interface for manipulating labels on an autotest server
    """
    ID_FIELD = ID_FIELD
    NAME_FIELD = NAME_FIELD
    FIELDS = ['atomic_group', 'invalid', 'kernel_config', 'only_if_needed',
              'platform']

    def __init__(self, connection, identification=None, name=None):
        super(Label, self).__init__(connection, identification, name)

    def _get_data_by_id(self):
        return get_data_by_id(self.connection, self.identification)

    def _get_data_by_name(self):
        return get_data_by_name(self.connection, self.name)


get_objs = functools.partial(arc.base.get_objs, get_ids_names, Label)
