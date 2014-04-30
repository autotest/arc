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
This module provides the argument parser that is used by the official CLI app
but can also be used by 3rd party apps.
"""


import os
import glob
import argparse
import importlib

import arc.defaults
import arc.cli.args.actions


__all__ = ['Parser']


class ConfigArgumentDefaultsHelpFormatter(argparse.HelpFormatter):

    '''
    Custom Help Formatter that also shows values from current configuration
    '''

    def _expand_help(self, action):
        '''
        Expands the help string, adding parameter names, choices, etc
        '''
        params = dict(vars(action), prog=self._prog)

        if hasattr(action, 'config_default'):
            params['config_default'] = action.config_default

        for name in list(params):
            if params[name] is argparse.SUPPRESS:
                del params[name]
        for name in list(params):
            if hasattr(params[name], '__name__'):
                params[name] = params[name].__name__
        if params.get('choices') is not None:
            choices_str = ', '.join([str(c) for c in params['choices']])
            params['choices'] = choices_str

        return self._get_help_string(action) % params

    def _get_help_string(self, action):
        '''
        Returns the modifed help string that includes the values on config
        '''
        hlp = action.help
        if '%(choices)' not in action.help:
            if hasattr(action, 'choices'):
                if action.choices is not None:
                    hlp += ' (%(choices)s)'

        if '%(default)' not in action.help:
            if hasattr(action, 'builtin_default'):
                if action.builtin_default is not argparse.SUPPRESS:
                    defaulting_nargs = [argparse.OPTIONAL,
                                        argparse.ZERO_OR_MORE]
                    if (action.option_strings or
                            action.nargs in defaulting_nargs):
                        if action.builtin_default is not None:
                            hlp += '. builtin default: %(builtin_default)s'
                    if hasattr(action, 'config_default'):
                        if action.config_default is not None:
                            if action.default is not None:
                                hlp += ','
                            hlp += ' default from config: %(config_default)s'
        return hlp


class ShortcutEnablerParser(argparse.ArgumentParser):

    '''
    Simple argument parser that does not care about choices and actual choice

    This is needed so that the *subparser* does not check the choices to given
    options before the ChoicesShortcutAction has the chance to actually set
    the full value based on the given (shortcut) value.
    '''

    def __init__(self, **kwargs):
        super(ShortcutEnablerParser, self).__init__(**kwargs)

    def _check_value(self, action, value):
        if action.__class__.__name__ == 'ChoicesShortcutAction':
            if action.number_of_matches(value) < 1:
                msg = ('given value "%s" does not match any choice, not even '
                       'when treating it as a shortcut' % value)
                raise argparse.ArgumentError(action, msg)
        else:
            argparse.ArgumentParser._check_value(self, action, value)


class Parser(argparse.ArgumentParser):

    '''
    The main CLI Argument Parser.
    '''

    def __init__(self, config=None):
        '''
        Initializes a new parser

        :param config: a class that implements the same features as
                       :class:`arc.config.Config`
        '''
        super(Parser, self).__init__(
            formatter_class=ConfigArgumentDefaultsHelpFormatter,
            description='Autotest RPC Client Command Line Interface App'
        )

        self.config = config
        self._subparsers = None
        self._add_global_arguments()

    def _add_global_arguments(self):
        '''
        Add global arguments, that is, do not depend on a specifc command
        '''
        server_group = self.add_argument_group('SERVER',
                                               'Autotest Server Selection')
        server_group.add_argument(
            '--host',
            help=('Hostname or IP address for the '
                  'autotest server'),
            default='localhost',
            action=arc.cli.args.actions.ConfigDefaultAction,
            config=self.config,
            config_section='server',
            config_key='host'
        )
        server_group.add_argument(
            '--username',
            help=('Username to login in autotest server'),
            action=arc.cli.args.actions.ConfigDefaultAction,
            config=self.config,
            config_section='server',
            config_key='username'
        )

    def add_arguments_on_all_modules(self,
                                     prefix=arc.defaults.ARGS_MODULE_PREFIX):
        '''
        Add arguments that are present on all Python modules at a given prefix

        :param prefix: a Python module namespace
        '''
        blacklist = ('actions', 'base', '__init__', 'parser')
        basemod = importlib.import_module(prefix)
        basemod_dir = os.path.dirname(basemod.__file__)

        # FIXME: This works for CPython and IronPython, but not for Jython
        mod_files_pattern = os.path.join(basemod_dir, "*.py")
        mod_files = glob.glob(mod_files_pattern)
        mod_names_with_suffix = [os.path.basename(f) for f in mod_files]
        mod_names = [n.replace(".py", "")
                     for n in mod_names_with_suffix]
        mod_names = [n for n in mod_names if n not in blacklist]

        for module in mod_names:
            self.add_arguments_on_module(module)

    def add_arguments_on_module(self, name):
        '''
        Add arguments that are present on a given Python module

        :param name: the name of the Python module, without the namespace
        '''
        if self._subparsers is None:
            self._subparsers = self.add_subparsers(
                prog='arcli',
                title='Top Level Command',
                dest='top_level_action',
                parser_class=ShortcutEnablerParser
            )

        module_name = "%s.%s" % (arc.defaults.ARGS_MODULE_PREFIX, name)
        module = importlib.import_module(module_name)

        parser = self._subparsers.add_parser(
            name,
            formatter_class=ConfigArgumentDefaultsHelpFormatter)
        if hasattr(module, 'ACTION_ARGUMENTS'):

            if module.ACTION_ARGUMENTS:
                act_grp = parser.add_argument_group("ACTION",
                                                    "Action to be performed")
                act_excl = act_grp.add_mutually_exclusive_group(required=True)

                for action in module.ACTION_ARGUMENTS:
                    act_excl.add_argument(*action[0], **action[1])

        if hasattr(module, 'ARGUMENTS'):
            if module.ARGUMENTS:
                for arg in module.ARGUMENTS:
                    # Add config instance to the options
                    if arg[1].get('config', None) == True:
                        arg[1]['config'] = self.config
                    # Support either both short+long options or either one, short OR long
                    short_and_or_long_opts = arg[0]
                    if len(short_and_or_long_opts) == 1:
                        parser.add_argument(arg[0][0], **arg[1])
                    else:
                        parser.add_argument(*arg[0], **arg[1])
