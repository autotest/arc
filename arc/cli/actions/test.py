"""
Module that implements the actions for the CLI App when the test toplevel
command is used
"""

import functools

import arc.cli.actions.base
import arc.test


OBJ_NAME = "test"


list_brief = functools.partial(arc.cli.actions.base.list_brief,
                               arc.test.get_objs)


delete = functools.partial(arc.cli.actions.base.delete,
                           OBJ_NAME, arc.test.Test, arc.test.delete)
