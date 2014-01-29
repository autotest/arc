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

import arc.connection
import arc.job


c = arc.connection.get_default()

# 1st approach, object like interface
print("Jobs List")
for job in arc.job.get_objs(c):
    print("%s\t%s" % (job.identification, job.name))

# 2nd approach, raw data manipulation
print("Jobs List")
for job in arc.job.get_data(c):
    print("%s\t%s" % (job["id"], job["name"]))
