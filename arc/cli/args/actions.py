"""
This module holds custom actions that are used to enhance the user experience
with the command line tool. Examples include actions that show the default
value for an option as set in the user's configuration file, actions that
allow the user to type less (shortcuts) and so on.
"""


import re
import argparse
import logging


__all__ = ['ConfigDefaultAction', 'ChoicesShortcutAction']


class ConfigDefaultAction(argparse.Action):
    """
    An argument action that optionally has a default set on a config file
    """
    def __init__(self, **kwargs):
        self.config = kwargs.pop('config', None)
        self.config_section = kwargs.pop('config_section', None)
        self.config_key = kwargs.pop('config_key', None)
        self.config_default = None

        super(ConfigDefaultAction, self).__init__(**kwargs)

        self.builtin_default = self.default
        if (self.config is not None and
            self.config.has_option(self.config_section,
                                   self.config_key)):
            self.config_default = self.config.get(self.config_section,
                                                  self.config_key)

        if self.config_default is not None:
            self.default = self.config_default
        else:
            self.default = self.builtin_default

        if (self.config_section is not None and
            self.config_key is not None):

            if self.metavar is None:
                self.metavar = self.config_key.upper()


    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values)


class ChoicesShortcutAction(ConfigDefaultAction):
    """
    Argument that allows for shorter input and also a config based default
    """
    def __init__(self, **kwargs):
        ConfigDefaultAction.__init__(self, **kwargs)


    def __call__(self, parser, namespace, value, option_string=None):
        if value not in self.choices:
            if self.unique_match(value):
                full_value = self.what_matches(value)
                logging.debug('Option value "%s" replaced by "%s"',
                              value, full_value)
                value = full_value
        ConfigDefaultAction.__call__(self, parser, namespace,
                                     value, option_string)


    def number_of_matches(self, shortcut):
        """
        Get the number of matches for the user supplied option string

        :param shortcut: the user supplied, usually incomplete option string
        """
        count = 0
        regex = re.compile(r'%s.*' % shortcut, re.I)
        for choice in self.choices:
            if regex.match(choice):
                count += 1
        return count


    def unique_match(self, shortcut):
        """
        Get whether the match for the user supplied option string in unique

        :param shortcut: the user supplied, usually incomplete option string
        """
        return self.number_of_matches(shortcut) == 1


    def what_matches(self, shortcut):
        """
        Get what the user supplied option string matches

        :param shortcut: the user supplied, usually incomplete option string
        """
        regex = re.compile(r'%s.*' % shortcut, re.I)
        assert self.unique_match(shortcut) == 1
        for choice in self.choices:
            if regex.match(choice):
                return choice
