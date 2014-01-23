"""
Module with interface for fetching and manipulating tests on a autotest server
"""


__all__ = ['get_data',
           'get_ids',
           'get_names',
           'get_ids_names',
           'get_data_by_id',
           'get_data_by_name',
           'get_control_file_by_id',
           'add',
           'delete',
           'modify',
           'Test',
           'get_objs']


import functools
import arc.base
import arc.shared.frontend


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
GET_METHOD = 'get_tests'
ADD_METHOD = 'add_test'
DELETE_METHOD = 'delete_test'
MODIFY_METHOD = 'modify_test'
CONTROL_FILE_METHOD = 'generate_control_file'


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
def add(connection, name, test_type, path):
    """
    FIXME: Currently has parameters only for the minimum required, later add
    all the optional parameters too
    returns: integer
    """
    return connection.run(SERVICE_NAME, ADD_METHOD, name, test_type, path)


def modify(connection, identification, **data):
    """
    """
    return connection.run(SERVICE_NAME, MODIFY_METHOD, identification, **data)


def get_control_file_by_id(connection, identification):
    """
    Get Control File for a test by passing its identification.

    :param connection: an instance of connection
    :param identification: a test identification
    :returns: the Control File (script) for the test
    """
    test = connection.run(SERVICE_NAME, CONTROL_FILE_METHOD,
                          tests=(identification,))
    return test['control_file']

class Test(arc.base.Model):
    """
    Interface for manipulating hosts on an autotest server
    """
    ID_FIELD = ID_FIELD
    NAME_FIELD = NAME_FIELD
    FIELDS = ['author', 'dependencies', 'description', 'experimental', 'path',
              'run_verify', 'sync_count', 'test_category', 'test_class',
              'test_time', 'test_type']

    def __init__(self, connection, identification=None, name=None):
        super(Test, self).__init__(connection, identification, name)

    def _get_data_by_id(self):
        return get_data_by_id(self.connection, self.identification)

    def _get_data_by_name(self):
        return get_data_by_name(self.connection, self.name)

    def __repr__(self):
        return "<Test Name: %s>" % self.name


get_objs = functools.partial(arc.base.get_objs, get_ids_names, Test)
