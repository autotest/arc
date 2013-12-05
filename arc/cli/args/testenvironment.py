"""
This module defines the command line arguments that will be available on
the arcli tool when the top level command (and module) server is executed
"""

__all__ = ['ACTION_ARGUMENTS', 'ARGUMENTS']


import arc.cli.args.base

#
# Arguments that are treated as actions
#
ARG_SHOW = (('-s', '--show'),
            {'help': 'show details about a test environment'})

ARG_DIFF = (('-d', '--diff'),
            {'help': 'shows differences between two test environments'})

ACTION_ARGUMENTS = [ARG_SHOW, ARG_DIFF]
