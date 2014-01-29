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
Module that implements the actions for the CLI App when the user toplevel
command is used
"""


import functools

import arc.cli.actions.base
import arc.user
import arc.utils


OBJ_NAME = "user"


list_brief = arc.cli.actions.base.action(
    functools.partial(arc.cli.actions.base.list_brief,
                      arc.user.get_objs))

list_full = arc.cli.actions.base.action(
    functools.partial(arc.cli.actions.base.list_full,
                      arc.user.get_objs))

add = arc.cli.actions.base.action(
    functools.partial(arc.cli.actions.base.add_with_name,
                      OBJ_NAME, arc.user.add))


delete = arc.cli.actions.base.action(
    functools.partial(arc.cli.actions.base.delete,
                      OBJ_NAME, arc.user.User, arc.user.delete))

def print_user(connection, user_id, show_all=False):
    user = arc.user.get_data_by_id(connection, user_id)
    if user:
        arc.utils.print_obj_content(user)

@arc.cli.actions.base.action
def show(app):
    print_user(app.connection,
               app.parsed_arguments.show)
