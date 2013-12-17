"""
Module that has base functions to implement actions of the CLI App

The functions defined here are usually not used directly, but specialized and
simplified via :func:`functools.partial`
"""

import arc.utils


__all__ = ['list_brief', 'list_full', 'add_with_name', 'delete', 'action',
           'get_identification']


def action(function):
    """
    Simple function that marks functions as CLI actions

    :param function: the function that will receive the CLI action mark
    """
    function.is_action = True
    return function


def list_brief(list_function, app, **filter_data):
    """
    Base function for briefly listing records

    This is usually not used directly, but simplified via
    :func:`functools.partial`

    :param name: name of the type of record, such as host, job, test, etc
    :param list_function: the function that will be used to retrieve records
    :param app: the running application instance
    """
    data = list_function(app.connection, **filter_data)
    arc.utils.print_objs_brief_as_table(data)


def list_full():
    """
    Base function for full listing records

    This is usually not used directly, but simplified via
    :func:`functools.partial`

    :param name: name of the type of record, such as host, job, test, etc
    :param list_function: the function that will be used to retrieve records
    :param app: the running application instance
    """
    data = list_function(app.connection, **filter_data)
    arc.utils.print_objs_as_table(data)


def add_with_name(name, add_function, app):
    """
    Base function for adding records that only require a name

    This is usually not used directly, but simplified via
    :func:`functools.partial`

    :param name: name of the type of record, such as host, job, test, etc
    :param list_function: the function that will be used to retrieve records
    :param app: the running application instance
    """
    if not app.parsed_arguments.name:
        app.log.error("Can not add a new %s without a proper name", name)
        return None

    return add_function(app.connection, app.parsed_arguments.name)


def delete(name, klass, delete_function, app):
    """
    Base function for deleting records by name or id

    This is usually not used directly, but simplified via
    :func:`functools.partial`

    :param name: name of the type of record, such as host, job, test, etc
    :param klass: the object class, inherited from :class:`arc.base.Model`
    :param delete_function: the function that will be used to delete records
    :param app: the running application instance
    """
    if not (app.parsed_arguments.name or app.parsed_arguments.id):
        app.log.error("Can not delete a %s without a name or id",
                      name)
        return

    if app.parsed_arguments.name:
        i = klass(app.connection, name=app.parsed_arguments.name)
        if not i.load_data():
            app.log.error("Could not find %s named %s",
                          name, app.parsed_arguments.name)
            return

    elif app.parsed_arguments.id:
        i = klass(app.connection,
                  identification=app.parsed_arguments.id)
        if not i.load_data():
            app.log.error("Could not find %s with id %s",
                          name, app.parsed_arguments.id)
            return

    return delete_function(app.connection, i.identification)


def delete_by_id(name, klass, delete_function, app):
    """
    Base function for deleting records by id

    This is usually not used directly, but simplified via
    :func:`functools.partial`

    :param name: name of the type of record, such as host, job, test, etc
    :param klass: the object class, inherited from :class:`arc.base.Model`
    :param delete_function: the function that will be used to delete records
    :param app: the running application instance
    """
    try:
        object_id = int(app.parsed_arguments.delete)
    except ValueError:
        object_id = app.parsed_arguments.id

    if not object_id:
        app.log.error("Can not delete a %s without an id", name)
        return

    i = klass(app.connection,
              identification=object_id)
    if not i.load_data():
        app.log.error("Could not find %s with id %s", name,
                      object_id)
        return

    return delete_function(app.connection, i.identification)


def get_identification(app):
    '''
    Get the identification from the command line opts, either name or id

    :param app: the running application instance
    '''
    if app.parsed_arguments.name:
        return app.parsed_arguments.name
    elif app.parsed_arguments.id:
        return app.parsed_arguments.id
    else:
        return None
