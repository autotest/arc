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
Atomic group actions for the CLI App when the atomicgroup toplevel
command is used.
"""


import functools

import arc.cli.actions.base
import arc.atomicgroup
import arc.utils


OBJ_NAME = "atomicgroup"


list_brief = arc.cli.actions.base.action(
    functools.partial(arc.cli.actions.base.list_brief,
                      arc.atomicgroup.get_objs))

list_full = arc.cli.actions.base.action(
    functools.partial(arc.cli.actions.base.list_full,
                      arc.atomicgroup.get_objs))

add = arc.cli.actions.base.action(
    functools.partial(arc.cli.actions.base.add_with_name,
                      OBJ_NAME, arc.atomicgroup.add))


delete = arc.cli.actions.base.action(
    functools.partial(arc.cli.actions.base.delete,
                      OBJ_NAME, arc.atomicgroup.AtomicGroup,
                      arc.atomicgroup.delete))

def print_atomicgroup(connection, atomicgroup_id, show_all=False):
    atomicgroup = arc.atomicgroup.get_data_by_id(connection, atomicgroup_id)
    if atomicgroup:
        arc.utils.print_obj_content(atomicgroup)

@arc.cli.actions.base.action
def show(app):
    print_atomicgroup(app.connection,
               app.parsed_arguments.show)
