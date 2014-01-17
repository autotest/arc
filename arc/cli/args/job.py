"""
This module defines the command line arguments that will be available on
the arcli tool when the top level command (and module) job is executed
"""

import argparse

import arc.constants
import arc.cli.args.actions
import arc.cli.args.base


__all__ = ['ARG_MACHINES',
           'ARG_CONTROL',
           'ARG_MACHINES',
           'ARG_TEST_TYPE',
           'ARG_EMAIL',
           'ARG_PRIORITY',
           'ARG_PROFILES',
           'ARG_REBOOT_BEFORE',
           'ARG_REBOOT_AFTER',
           'ARG_RUNNING',
           'ACTION_ARGUMENTS',
           'ARGUMENTS']


#
# Individual arguments that can be re-used elsewhere
#
ARG_CONTROL = (('-c', '--control-file'),
               {'help': 'path to the control file defining the job',
                'type': argparse.FileType('r')})

ARG_MACHINES = (('-m', '--machines'),
                {'help': ('the machine specification on where to run the '
                          'test, either a list of machines or n*label'),
                 'action': arc.cli.args.actions.ConfigDefaultAction,
                 'config': True,
                 'config_section': 'job',
                 'config_key': 'machines'})

ARG_TEST_TYPE = (('-t', '--test-type'),
                 {'help': 'the type of test',
                  'choices': arc.constants.TEST_VALID_TYPES,
                  'action': arc.cli.args.actions.ChoicesShortcutAction,
                  'default': arc.constants.TEST_VALID_TYPES[0],
                  'config': True,
                  'config_section': 'job',
                  'config_key': 'test_type'})

ARG_EMAIL = (('-e', '--email'),
             {'help': ('A comma seperated list of email addresses to notify '
                       'of job completion'),
              'action': arc.cli.args.actions.ConfigDefaultAction,
              'config': True,
              'config_section': 'job',
              'config_key': 'email'})

ARG_PRIORITY = (('-p', '--priority'),
                {'help': 'the priority of test, used by the scheduler',
                 'choices': arc.constants.JOB_PRIORITIES,
                 'action': arc.cli.args.actions.ChoicesShortcutAction,
                 'default': arc.constants.JOB_PRIORITIES[2],
                 'config': True,
                 'config_section': 'job',
                 'config_key': 'priority'})

ARG_PROFILES = (('-P', '--profiles'),
                {'help': 'the list of profiles for the hosts',
                 'action': 'append',
                 'default': []})

ARG_REBOOT_BEFORE = (('-B', '--reboot-before'),
                     {'help': ('Should test machines be rebooted before the '
                               'job execution?'),
                      'choices': arc.constants.JOB_VALID_REBOOT_BEFORE,
                      'action': arc.cli.args.actions.ChoicesShortcutAction,
                      'default': arc.constants.JOB_VALID_REBOOT_BEFORE[0],
                      'config': True,
                      'config_section': 'job',
                      'config_key': 'reboot_before'})

ARG_REBOOT_AFTER = (('-A', '--reboot-after'),
                    {'help': ('Should test machines be rebooted after the '
                              'job execution?'),
                     'choices': arc.constants.JOB_VALID_REBOOT_AFTER,
                     'action': arc.cli.args.actions.ChoicesShortcutAction,
                     'default': arc.constants.JOB_VALID_REBOOT_AFTER[0],
                     'config': True,
                     'config_section': 'job',
                     'config_key': 'reboot_after'})

ARG_RUNNING = (('--all',),
               {'help': ('Show all information. Either show all jobs or all '
                         'information about a given job. Depends on the '
                         'given command'),
                'action': 'store_true',
                'default': False})

ARG_FROM_TEST = (('-T', '--from-test-number'),
                 {'help': ('Add (create) a new job using the control file'
                  'from a test registered on the autotest server'),
                  'type': int,
                  'metavar': 'TEST_ID'})

ARG_EDIT_BEFORE = (('-E', '--edit-before-sending', ),
                   {'help': ('Open control file in editor before sending '
                             'the control file to the server.'),
                    'action': 'store_true',
                    'default': False})


#
# Action arguments
#
ACTION_ADD = (('-a', '--add'),
              {'help': 'add (create) a new job',
               'action': 'store_true',
               'default': False})

ACTION_DELETE = (('-d', '--delete'),
                 {'help': 'delete (abort) a queued or running job',
                  'default': False,
                  'metavar': 'JOB_ID'})

ACTION_SHOW = (('-s', '--show'),
               {'help': 'shows details about a job',
                'default': False,
                'type' : int,
                'metavar': 'JOB_ID'})

#
# Arguments that are treated as actions
#
ACTION_ARGUMENTS = [arc.cli.args.base.LIST_BRIEF,
                    ACTION_ADD,
                    ACTION_DELETE,
                    ACTION_SHOW]


#
# Other arguments that will influence action behaviour
#
ARGUMENTS = [arc.cli.args.base.NAME,
             arc.cli.args.base.ID,
             ARG_CONTROL,
             ARG_TEST_TYPE,
             ARG_MACHINES,
             ARG_EMAIL,
             ARG_PRIORITY,
             ARG_PROFILES,
             ARG_REBOOT_BEFORE,
             ARG_REBOOT_AFTER,
             ARG_RUNNING,
             ARG_FROM_TEST,
             ARG_EDIT_BEFORE]
