"""
This module defines the command line arguments that will be available on
the arcli tool when the top level command (and module) label is executed
"""


__all__ = ['ARG_NAME',
           'ARG_ID',
           'ACTION_ARGUMENTS',
           'ARGUMENTS']


import arc.cli.args.base


#
# Individual arguments that can be re-used elsewhere
#
ARG_NAME = (('-n', '--name'),
            {'help': 'name of the label to manipulated'})


ARG_ID = (('-i', '--id'),
          {'help': 'numeric identification of the label to manipulated'})


#
# Arguments that are treated as actions
#
ACTION_ARGUMENTS = [arc.cli.args.base.LIST_BRIEF,
                    arc.cli.args.base.ADD,
                    arc.cli.args.base.DELETE]


#
# Other arguments that will influence action behaviour
#
ARGUMENTS = [ARG_NAME, ARG_ID]
