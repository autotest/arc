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

import arc.server
import arc.connection

c = arc.connection.get_default()
status = arc.server.get_status(c)

print("Concerns: %s" % status["concerns"])
print("Scheduler Running: %s" % status["scheduler_running"])
print("Scheduler Watcher Running: %s" % status["scheduler_watcher_running"])
print("Install Server Running: %s" % status["install_server_running"])
print("Log Disk Space Usage: %s%%" % status["used_space_logs"])
