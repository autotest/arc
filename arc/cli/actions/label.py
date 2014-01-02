"""
Module that implements the actions for the CLI App when the label toplevel
command is used
"""


import functools

import arc.cli.actions.base
import arc.label


OBJ_NAME = "label"


list_brief = arc.cli.actions.base.action(
    functools.partial(arc.cli.actions.base.list_brief,
                      arc.label.get_objs))


list_full = arc.cli.actions.base.action(
    functools.partial(arc.cli.actions.base.list_full,
                      arc.label.get_objs))


add = arc.cli.actions.base.action(
    functools.partial(arc.cli.actions.base.add_with_name,
                      OBJ_NAME, arc.label.add))


delete = arc.cli.actions.base.action(
    functools.partial(arc.cli.actions.base.delete,
                      OBJ_NAME, arc.label.Label, arc.label.delete))
