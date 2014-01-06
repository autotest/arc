"""
This module defines the command line arguments that will be available on
the arcli tool when the top level command (and module) server is executed
"""

__all__ = ['ACTION_ARGUMENTS']


#
# Arguments that are treated as actions
#
ARG_STATUS = (('-s', '--status'),
              {'help': 'obtain the status of the Autotest server',
               'action': 'store_true',
               'default': False})

ARG_PROFILES = (('-l', '--list-install-profiles'),
                {'help': 'list the available installation profiles',
                 'action': 'store_true',
                 'default': False})

ACTION_ARGUMENTS = [ARG_STATUS, ARG_PROFILES]
