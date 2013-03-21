"""
Module with interface for fetching and manipulating hosts on a autotest server
"""

import re
import functools

import arc.base
import arc.defaults
import arc.label


__all__ = ['get_data',
           'get_ids',
           'get_names',
           'get_ids_names',
           'get_data_by_id',
           'get_data_by_name',
           'add',
           'delete',
           'modify',
           'reverify',
           'Host',
           'get_objs']


#
# Service on RPC server hosting these methods
#
SERVICE_NAME = arc.defaults.AFE_SERVICE_NAME


#
# Name of fields as defined on the server side database
#
ID_FIELD = 'id'
NAME_FIELD = 'hostname'


#
# Name of RPC methods as defined on the server side
#
GET_METHOD = 'get_hosts'
ADD_METHOD = 'add_host'
DELETE_METHOD = 'delete_host'
MODIFY_METHOD = 'modify_host'


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
def add(connection, name, status=None, locked=None, protection=None):
    """
    Add a new host entry

    :param connection:
    :param name:
    :param status:
    :param locked:
    :param protection:
    :return: integer that is the identification of the newly added host
    """
    return connection.run(SERVICE_NAME, ADD_METHOD,
                          name, status, locked, protection)


def modify(connection, identification, **data):
    """ 
   Modify a host entry

    :param connection:
    :param identification:
    :param data:
    """
    return connection.run(SERVICE_NAME, MODIFY_METHOD,
                          identification, **data)


def reverify(connection, identification):
    data = {'hostname': identification}
    return connection.run(SERVICE_NAME, 'reverify_hosts', **data)


def add_labels(connection, identification, labels_identification):
    connection.run(SERVICE_NAME, 'host_add_labels',
                   identification, labels_identification)


class Host(arc.base.Model):
    """
    Interface for manipulating hosts on an autotest server
    """
    ID_FIELD = ID_FIELD
    NAME_FIELD = NAME_FIELD
    FIELDS = ['acls', 'atomic_group', 'attributes', 'current_profile', 'dirty',
              'invalid', 'labels', 'lock_time', 'locked', 'locked_by',
              'platform', 'profiles', 'protection', 'status', 'synch_id']


    def __init__(self, connection, identification=None, name=None):
        super(Host, self).__init__(connection,
                                   identification,
                                   name)


    def _get_data_by_id(self):
        return get_data_by_id(self.connection, self.identification)


    def _get_data_by_name(self):
        return get_data_by_name(self.connection, self.name)


    def get_label_data(self):
        """
        Get raw data on this host's labels
        """
        return arc.label.get_data(self.connection,
                                  host__id=self.identification)


    def get_label_names(self):
        """
        Get this host's labels names
        """
        return [i.get("name") for i in self.get_label_data()]


    def __repr__(self):
        return "<Host Name: %s>" % self.name


get_objs = functools.partial(arc.base.get_objs,
                             get_ids_names,
                             Host)


def parse_meta_host_labels(connection, label):
    """
    Parse the label part of the meta_host definition

    If it has a wild card it gets expanded into a list of all matching labels,
    e.g.: 2*label* becomes 2*label1 2*label2 2*label3
    """
    if label.endswith('*'):
        labels = connection.run('get_labels',
                                name__startswith=label.rstrip('*'))
        return [l['name'] for l in labels]
    else:
        return [label]


def parse_specification(connection, host_specification):
    """
    Parse a host specification and return hosts and meta_hosts

    A host is a regular name, a meta_host is n*label or *label.
    """
    hosts = []
    meta_hosts = []

    if re.match('^[0-9]+[*]', host_specification):
        num, host = host_specification.split('*', 1)
        meta_hosts += int(num) * parse_meta_host_labels(connection, host)

    elif re.match('^[*](\w*)', host_specification):
        group1 = re.match('^[*](\w*)', host).group(1)
        meta_hosts += parse_meta_host_labels(connection, group1)

    elif host_specification != '' and host_specification not in hosts:
        # Real hostname and not a duplicate
        hosts.append(host_specification)

    return (hosts, meta_hosts)


def parse_specifications(connection, host_specifications):
    """
    Parse a list of host specification and return hosts and meta_hosts

    A host is a regular name, a meta_host is n*label or *label.
    """
    hosts = []
    meta_hosts = []

    for host_specification in host_specifications:
        l_hosts, l_meta_hosts = parse_specification(connection,
                                                    host_specification)
        if l_hosts not in hosts:
            hosts += l_hosts
        if l_meta_hosts not in meta_hosts:
            meta_hosts += l_meta_hosts

    return (hosts, meta_hosts)
