"""
Module with interface for fetching users on an autotest server
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
           'User',
           'get_objs']


#
# Service on RPC server hosting these methods
#
SERVICE_NAME = arc.shared.frontend.AFE_SERVICE_NAME


#
# Name of fields as defined on the server side database
#
ID_FIELD = 'id'
NAME_FIELD = 'login'


#
# Name of RPC methods as defined on the server side
#
GET_METHOD = 'get_users'
ADD_METHOD = 'add_user'
DELETE_METHOD = 'delete_user'
MODIFY_METHOD = 'modify_user'


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


#
# Methods that have add more logic related to the manipulated object nature
#
def add(connection, login, access_level=None):
    """
    Add a new user entry

    :param connection:
    :param login:
    :param access_level:
    """
    return connection.run(SERVICE_NAME, ADD_METHOD, login, access_level)

def modify(connection, user_id, **data):
    """
    Modify an user entry

    :param connection:
    :param user_id:
    :param data:
    """
    return connection.run(SERVICE_NAME, MODIFY_METHOD, user_id, **data)

def delete(connection, user_id):
    """
    Delete an user entry

    :param connection:
    :param user_id:
    """
    return connection.run(SERVICE_NAME, DELETE_METHOD, user_id)


class User(arc.base.Model):
    """
    Interface for manipulating users on an autotest server
    """
    ID_FIELD = ID_FIELD
    NAME_FIELD = NAME_FIELD
    FIELDS = ['access_level', 'reboot_before', 'reboot_after',
              'drone_set', 'show_experimental']

    def __init__(self, connection, identification=None, name=None):
        super(User, self).__init__(connection, identification, name)

    def _get_data_by_id(self):
        return get_data_by_id(self.connection, self.identification)

    def _get_data_by_name(self):
        return get_data_by_name(self.connection, self.name)


get_objs = functools.partial(arc.base.get_objs, get_ids_names, User)
