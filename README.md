arc
===

Autotest RPC Client is a pure Python library that servers as the client part of
Autotest's[1] server interface. It aims to be:

 * Really portable

   - Across Python versions and implementations
   - Only depend on Python Standard Library

 * Extensible

   - Allowing you to make both the API and applications behave the way you want
     or get more features


 * Intuitive

   - Very low curve to writing custom client apps
   - Documentation and samples for both API and CLI users


The current release
===================

The current release of arc is not yet supposed to be feature complete and
deprecate the old autotest-rpc-client (autotest/cli) code just yet, but will
eventually do so.


What's Included
---------------

 * A simple but handy JSON model, allowing one to fetch and access data from
   the Autotest RPC Server in a easy way.

 * A configuration class that allows for both global and user specific
   configuration. This is handy for having a global configuration file
   installed by a package, but still allow the individual user to override
   their values.

 * A command line tool, currently named "arcli", that adds a thin layer on
   top of the API. It currently exposes actions such as listing, creating
   and deleting objects from Autotest RPC Server. Say, to add a new host::

   # arcli host -c -n newhost.mydomain.org

   And to list all the jobs::

   # arcli job -l

   To list only the currently running jobs::

   # arcli job -l --running

 * Integration between command line arguments and values already specified
   in the configuration file. This allows a user to have in his configuration
   the default values that would be otherwise passed via the command line.
   No need for repeating the same option again and again.

 * Integration between RPC definitions and command line arguments. That means
   that values that are expected to be sent to the server, are directly used
   on the command line.

 * Shortcuts on command line options: since literals expected by the RPC server
   are often lengthy, such as "If all tests passed" for the "-A/--reboot-after"
   job option, the CLI tool has a feature that allows you to simply use::

   # arcli job -a -Ai ...

   If "i" uniquely distinguishes one of the RPC literals, it's going to be
   substituted by it. This allows less code duplication and quicker command
   entries.

 * Portability: even though CPython itself is already portable, arc aims to
   be even more portable. It has been tested on:

   - CPython 2.7
   - CPython 3.3
   - Jython 2.7
   - IronPython 2.7 via mono

[1] http://autotest.github.com
