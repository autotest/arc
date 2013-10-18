"""
This module defines the command line arguments that will be available on
the arcli tool when the top level command (and module) server is executed
"""

__all__ = ['ACTION_ARGUMENTS', 'ARGUMENTS']


import arc.cli.args.base

#
# Arguments that are treated as actions
#
ARG_STATUS = (('-f', '--find'),
              {'help': 'find the last point where a test begin failing',
               'action': 'store_true',
               'default': False})


ACTION_ARGUMENTS = [ARG_STATUS]

ARGUMENTS = [arc.cli.args.base.NAME]
