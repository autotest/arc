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
