"""
Module that has base functions to manipulate JSON data from RPC services

The functions defined here are usually not used directly, but specialized and
simplified via :func:`functools.partial`
"""


__all__ = ['get_by',
           'get_and_filter',
           'delete',
           'Model']


import arc.defaults


def get_data(service, method, connection, **data_filter):
    """
    Base function to fetch data from the RPC server

    This is usually not used directly, but simplified via
    :func:`functools.partial`
    """
    return connection.run(service, method, **data_filter)


def get_by(service, method, field, connection, value=None):
    """
    Base function to fetch data from the RPC server using a single field filter

    This is usually not used directly, but simplified via
    :func:`functools.partial`
    """
    data_filter = {field: value}
    data = connection.run(service, method, **data_filter)
    if len(data) == 1:
        return data[0]
    return None


def get_and_filter(function, field, connection, **data_filter):
    """
    Base function to fetch and filter data from the RPC server

    This is usually not used directly, but simplified via
    :func:`functools.partial`
    """
    data = function(connection, **data_filter)
    return (i.get(field) for i in data)


def get_id_name_and_filter(function, id_field, name_field,
                           connection, **data_filter):
    """
    Base function to fetch and filter data from the RPC server

    This is usually not used directly, but simplified via
    :func:`functools.partial`
    """
    data = function(connection, **data_filter)
    return ((i.get(id_field), i.get(name_field)) for i in data)


def get_objs(function, klass, connection, **data_filter):
    """
    Base function to get data as objects that inherit from Model

    This is usually not used directly, but simplified via functools.partial()
    """
    for (identification, name) in function(connection, **data_filter):
        yield klass(connection,
                    identification=identification,
                    name=name)


def delete(service, method, connection, identification):
    """
    Base function to delete an object from the RPC server

    This is usually not used directly, but simplified via
    :func:`functools.partial`
    """
    return connection.run(service, method, identification)


class Model(object):
    """
    Base class for modeling objects from the RPC server JSON data
    """

    ID_FIELD = 'id'
    NAME_FIELD = 'name'
    FIELDS = []

    AUTOLOAD = True

    def __init__(self, connection, identification=None, name=None):
        self.connection = connection
        self.identification = identification
        self.name = name
        self.data = None
        self.data_loaded = False

        if self.AUTOLOAD:
            if not (self.identification is not None and
                    self.name is not None):
                self.data_loaded = self.load_data()

    def _get_data_by_id(self):
        """
        Fetch a single object data by its id
        """
        raise NotImplementedError

    def _get_data_by_name(self):
        """
        Fetch a single object data by its name
        """
        raise NotImplementedError

    def get_data(self):
        """
        Fetch object data based on either id or name, as set on this object
        """
        data = None
        if self.identification is not None:
            try:
                data = self._get_data_by_id()
            except NotImplementedError:
                data = None

        if data is None and self.name is not None:
            try:
                data = self._get_data_by_name()
            except NotImplementedError:
                data = None

        if data is not None:
            if self.NAME_FIELD in data:
                self.name = data[self.NAME_FIELD]

            if self.ID_FIELD in data:
                self.identification = data[self.ID_FIELD]

        return data

    def load_data(self):
        """
        Loads this object's data and flags if data was successfully fetched
        """
        data = self.get_data()
        if data is None:
            return False

        self.data = data
        return True

    def __getattr__(self, attr):
        if attr in self.FIELDS:
            if self.AUTOLOAD:
                if not self.data_loaded:
                    self.data_loaded = self.load_data()

            if self.data is not None:
                return self.data[attr]
