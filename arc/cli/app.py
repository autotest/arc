#!/usr/bin/env/python


"""
This is the main entry point for the ARC cli application
"""


import logging
import importlib

import arc.config
import arc.connection
import arc.defaults
import arc.cli.args.parser


__all__ = ['App']


class App(object):
    """
    Base class for CLI application
    """
    def __init__(self, config_klass=None, argument_parser_klass=None):
        """
        Initializes a new app instance.

        This class is intended both to be used by the stock arcli application
        and also to be reused by custom applications. If you want, say, to
        limit the amount of command line actions and its arguments, you can
        simply supply another argument parser class to this constructor. Of
        course another way to customize it is to inherit from this and modify
        its members at will.

        :param config_klass: an optional configuration class. By default it
               will use the arc.config.Config class.
        :param argument_parser_klass: an optional argument parser class. By
               default it will use arc.cli.args.parser.Parser
        """
        #: The application holds a connection instance so that other actions
        #: can simply use an already initialized connection for convenience
        self.connection = None

        self.log = None
        self._initialize_log()

        self.config = None
        self.config_klass = config_klass
        self._initialize_config()

        self.argument_parser = None
        self.argument_parser_klass = argument_parser_klass
        self.parsed_arguments = None
        self._initialize_argument_parser()


    def _initialize_log(self):
        """
        Initializes a log instance based on the class name
        """
        logging.basicConfig()
        self.log = logging.getLogger(self.__class__.__name__)


    def _initialize_config(self):
        """
        Initializes the configuration system

        We keep track of the configuration class used in case it was overriden
        """
        if self.config_klass is None:
            self.log.debug("Initializing default config class")
            self.config = arc.config.get_default()
        else:
            self.log.debug("Initializing user supplied config class: %s",
                           self.config_klass)
            self.config = self.config_klass()


    def _initialize_argument_parser(self):
        """
        Initialize the argument parser, either the default or supplied one
        """
        if self.argument_parser_klass is None:
            self.log.debug("Initializing default argument parser class")
            self.argument_parser = arc.cli.args.parser.Parser(self.config)
            self.argument_parser.add_arguments_on_all_modules()
        else:
            self.log.debug("Initializing user supplied argument parser class:"
                           " %s", self.argument_parser_klass)
            self.argument_parser = self.argument_parser_klass(self.config)


    def parse_arguments(self):
        """
        Parse the arguments from the command line
        """
        self.parsed_arguments = self.argument_parser.parse_args()
        if hasattr(self.parsed_arguments, "top_level_action"):
            self.log.debug("Action (subparser): %s",
                           self.parsed_arguments.top_level_action)


    def initialize_connection(self):
        """
        Initialize the connection instance
        """
        if self.connection is not None:
            self.log.debug("Connection is already initialized")
        else:
            if hasattr(self.parsed_arguments, "host"):
                h = self.parsed_arguments.host
                self.log.debug("Connecting to: %s", h)
                self.connection = arc.connection.Connection(h)
                if not self.connection.ping():
                    self.log.error("Could not validate connection to server")
                    raise SystemExit
            else:
                self.log.warn("Host setting not present on arguments, not "
                              "initializing a connection")


    def dispatch_action(self):
        """
        Calls the actions that was specified via command line arguments.

        This involves loading the relevant module file.
        """
        module_name = "%s.%s" % (arc.defaults.ACTIONS_MODULE_PREFIX,
                                 self.parsed_arguments.top_level_action)
        self.log.debug("Attempting to load action module: %s", module_name)

        try:
            module = importlib.import_module(module_name)
            self.log.debug("Action module loaded: %s", module)
        except ImportError:
            self.log.critical("Could not load action module: %s", module_name)
            return

        # FIXME: this needs a better instrospection of the action arguments
        # exclusive group, so that all action arguments are picked up here
        # make list the default action
        action = 'list_brief'
        if self.parsed_arguments.list_brief:
            action = 'list_brief'
        elif self.parsed_arguments.add:
            action = 'add'
        elif self.parsed_arguments.delete:
            action = 'delete'
        elif self.parsed_arguments.modify:
            action = 'modify'

        if hasattr(module, action):
            self.log.debug("Calling action %s from module %s",
                           action, module_name)
            kallable = getattr(module, action)
            self.initialize_connection()
            kallable(self)
        else:
            self.log.error("Action %s specified, but not implemented", action)


    def run(self):
        """
        Main entry point for application
        """
        self.parse_arguments()
        self.dispatch_action()
