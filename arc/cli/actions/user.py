"""
Module that implements the actions for the CLI App when the user toplevel
command is used
"""


import functools

import arc.cli.actions.base
import arc.user


OBJ_NAME = "user"


list_brief = arc.cli.actions.base.action(
    functools.partial(arc.cli.actions.base.list_brief,
                      arc.user.get_objs))
