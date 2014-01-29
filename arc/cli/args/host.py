# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
# See LICENSE for more details.
#
# Copyright (c) 2013-2014 Red Hat
# Author: Cleber Rosa <cleber@redhat.com>

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
            {'help': 'name, usually the FQDN'})


ARG_ID = (('-i', '--id'),
          {'help': 'numeric identification of the host',
           'type': int})


#
# Arguments that are treated as actions
#
ARG_LIST_JOBS = (('-j', '--list-jobs'),
                 {'help': 'list the jobs running on the listed hosts',
                  'action': 'store_true',
                  'default': False})


ARG_LOCK = (('--lock', ),
            {'help': 'locks the host (makes it unavailable to new jobs)',
             'action': 'store_true'})


ARG_UNLOCK = (('--unlock', ),
              {'help': 'unlocks the host (makes it available to new jobs)',
               'action': 'store_true'})


ARG_REVERIFY = (('--reverify', ),
                {'help': 'schedules a host reverification job',
                 'action': 'store_true'})


ACTION_ARGUMENTS = [arc.cli.args.base.LIST_BRIEF,
                    ARG_LIST_JOBS,
                    arc.cli.args.base.ADD,
                    arc.cli.args.base.DELETE,
                    ARG_LOCK,
                    ARG_UNLOCK,
                    ARG_REVERIFY]


#
# Other arguments that will influence action behaviour
#
ARGUMENTS = [ARG_NAME, ARG_ID]
