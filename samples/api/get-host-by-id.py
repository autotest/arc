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

import sys

import arc.connection
import arc.host


host_id = sys.argv[1]

c = arc.connection.get_default()
h = arc.host.get_data_by_id(c, host_id)
if h is not None:
    print("Found host with id %s, name is %s" % (host_id,
                                                 h['hostname']))
