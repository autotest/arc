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
                    arc.cli.args.base.ADD,
                    arc.cli.args.base.DELETE]


#
# Other arguments that will influence action behaviour
#
ARGUMENTS = [arc.cli.args.base.NAME, arc.cli.args.base.ID]
