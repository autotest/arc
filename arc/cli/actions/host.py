"""
Module that implements the actions for the CLI App when the host toplevel
command is used
"""


import functools

import arc.cli.actions.base
import arc.host


OBJ_NAME = "host"


list_brief = functools.partial(arc.cli.actions.base.list_brief,
                               arc.host.get_objs)


add = functools.partial(arc.cli.actions.base.add_with_name,
                        OBJ_NAME, arc.host.add)


delete = functools.partial(arc.cli.actions.base.delete,
                           OBJ_NAME, arc.host.Host, arc.host.delete)
