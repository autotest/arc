"""
This is the main entry point for the ARC cli application
"""


import sys
import types
import logging
import importlib
import functools

import arc.config
import arc.connection
import arc.defaults
import arc.cli.args.parser

from urllib2 import URLError

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
                try:
                    self.connection = arc.connection.Connection(h)
                except arc.connection.InvalidServiceVersionError:
                    self.log.error("The RPC interface version on the connected "
                                   "server is more recent than this version of "
                                   "arc can support. Please use a more recent "
                                   "version of arc that should include support "
                                   "for the latest Autotest version.")
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

        # Filter out the attributes out of the loaded module that look
        # like command line actions, based on type and 'is_action' attribute
        module_actions = {}
        for attribute_name in module.__dict__:
            attribute = module.__dict__[attribute_name]
            if (isinstance(attribute, types.FunctionType) or
                    isinstance(attribute, functools.partial)):
                if hasattr(attribute, 'is_action'):
                    if attribute.is_action:
                        module_actions[attribute_name] = attribute

        chosen_action = None
        for action in module_actions.keys():
            if getattr(self.parsed_arguments, action, False):
                self.log.debug("Calling action %s from module %s",
                               action, module_name)
                chosen_action = action
                break

        kallable = module_actions.get(chosen_action, None)
        if kallable is not None:
            self.initialize_connection()
            return kallable(self)
        else:
            self.log.error("Action %s specified, but not implemented",
                           chosen_action)

    def run(self):
        """
        Main entry point for application
        """
        action_result = None
        try:
            self.parse_arguments()
            action_result = self.dispatch_action()
        except KeyboardInterrupt:
            print 'Interrupted'
        except URLError as e:
            self.log.error(e)
        except arc.proxy.RPCError as e:
            msg = e.message.split('\n')
            self.log.error(msg[0])
        if isinstance(action_result, int):
            sys.exit(action_result)
        elif isinstance(action_result, bool):
            if action_result is True:
                sys.exit(0)
            else:
                sys.exit(1)
