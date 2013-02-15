"""
This module defines the command line arguments that will be available on
the arcli tool when the top level command (and module) host is executed
"""


import arc.cli.args.base


__all__ = ['ARG_NAME',
           'ARG_ID',
           'ACTION_ARGUMENTS',
           'ARGUMENTS']


#
# Individual arguments that can be re-used elsewhere
#
ARG_NAME = (('-n', '--name'),
            {'help': 'name (usually the FQDN) of the host to manipulated'})


ARG_ID = (('-i', '--id'),
          {'help': 'numeric identification of the host to manipulated'})


#
# Arguments that are treated as actions
#
ARG_LIST_JOBS = (('-j', '--list-jobs'),
                 {'help': 'list the jobs running on the listed hosts',
                  'action': 'store_true',
                  'default': False})


ACTION_ARGUMENTS = [arc.cli.args.base.LIST_BRIEF,
                    ARG_LIST_JOBS,
                    arc.cli.args.base.ADD,
                    arc.cli.args.base.DELETE]


#
# Other arguments that will influence action behaviour
#
ARGUMENTS = [ARG_NAME, ARG_ID]
