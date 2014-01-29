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
# Copyright (c) 2013-2014 Red Hat
# Author: Cleber Rosa <cleber@redhat.com>

'''
Basic definitions for the rpc services.
'''

import frontend

__all__ = ['DEFAULT_PATH',
           'AFE_PATH',
           'TKO_PATH',
           'PATHS']

#: RPC path to use for unknown service
DEFAULT_PATH = '/'

#: RPC path for the AFE service
AFE_PATH = "%srpc/" % frontend.AFE_URL_PREFIX

#: RPC path for the TKO service
TKO_PATH = "%srpc/" % frontend.TKO_URL_PREFIX

#: The service available on a regular Autotest RPC server and their RPC PATHS
PATHS = {frontend.AFE_SERVICE_NAME: AFE_PATH,
         frontend.TKO_SERVICE_NAME: TKO_PATH}
