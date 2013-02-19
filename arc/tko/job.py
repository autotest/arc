"""
Module with interface for fetching and manipulating tko jobs on a autotest
server.
"""


import functools

import arc.base
import arc.defaults


__all__ = ['get_data']


#
# Service on RPC server hosting these methods
#
SERVICE_NAME = arc.defaults.TKO_SERVICE_NAME


#
# Name of fields as defined on the server side database
#
ID_FIELD = 'id'
NAME_FIELD = 'tag'


#
# Name of RPC methods as defined on the server side
#
GET_METHOD = 'get_jobs'


#
# Boiler plate code for remote methods that are generic enough to be reused
#
get_data = functools.partial(arc.base.get_data, SERVICE_NAME, GET_METHOD)
