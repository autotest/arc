"""
This module defines the command line arguments that will be available on
the arcli tool when the top level command (and module) user is executed
"""


__all__ = ['ACTION_ARGUMENTS',
           'ARGUMENTS']


import arc.cli.args.base

#
# Action arguments
#
ACTION_SHOW = (('-s', '--show'),
               {'help': 'shows details about an user',
                'default': False,
                'type': int,
                'metavar': 'USER_ID'})


#
# Arguments that are treated as actions
#
ACTION_ARGUMENTS = [arc.cli.args.base.LIST_BRIEF,
                    arc.cli.args.base.LIST_FULL,
                    arc.cli.args.base.ADD,
                    #arc.cli.args.base.MODIFY,
                    arc.cli.args.base.DELETE,
                    ACTION_SHOW]


#
# Other arguments that will influence action behaviour
#
ARGUMENTS = [arc.cli.args.base.NAME, arc.cli.args.base.ID]
