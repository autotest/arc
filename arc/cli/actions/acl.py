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
# Copyright (c) 2014 Red Hat
# Author: Ruda Moura <rmoura@redhat.com>

"""
Module that implements the actions for the CLI App when the acl toplevel
command is used
"""


import functools

import arc.cli.actions.base
import arc.acl


OBJ_NAME = "acl"


list_brief = arc.cli.actions.base.action(
    functools.partial(arc.cli.actions.base.list_brief,
                      arc.acl.get_objs))


list_full = arc.cli.actions.base.action(
    functools.partial(arc.cli.actions.base.list_full,
                      arc.acl.get_objs))


add = arc.cli.actions.base.action(
    functools.partial(arc.cli.actions.base.add_with_name,
                      OBJ_NAME, arc.acl.add))


delete = arc.cli.actions.base.action(
    functools.partial(arc.cli.actions.base.delete,
                      OBJ_NAME, arc.acl.AclGroup, arc.acl.delete))
