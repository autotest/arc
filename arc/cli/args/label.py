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

"""
This module defines the command line arguments that will be available on
the arcli tool when the top level command (and module) label is executed
"""


__all__ = ['ACTION_ARGUMENTS',
           'ARGUMENTS']


import arc.cli.args.base


#
# Arguments that are treated as actions
#
ACTION_ARGUMENTS = [arc.cli.args.base.LIST_BRIEF,
                    arc.cli.args.base.LIST_FULL,
                    arc.cli.args.base.ADD,
                    arc.cli.args.base.DELETE]


#
# Other arguments that will influence action behaviour
#
ARGUMENTS = [arc.cli.args.base.NAME, arc.cli.args.base.ID]
