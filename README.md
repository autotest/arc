arc
===

Autotest RPC Client is a pure Python library that servers as the client part of
Autotest's[1] server interface. It aims to be:

* Really portable
  - Across Python versions and implementations
  - Only depend on Python Standard Library

 * Extensible
   - Allowing you to make both the API and applications behave the way you
     want or get more features

 * Intuitive
   - Very low curve to writing custom client apps
   - Documentation and samples for both API and CLI users


This initial release
====================

This is the first release of arc. It's not supposed to be feature complete and
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

 * Integration between command line arguments and values already specified
   in the configuration file. This allows a user to have in his configuration
   the default values that would be otherwise passed via the command line.
   No need for repeating the same option again and again.

 * Integration between RPC definitions and command line arguments. That means
   that values that are expected to be sent to the server, are directly used
   on the command line.

 * Shortcuts on command line options: since literals expected by the RPC server
   are often lengthy, such as "If all tests passed" for the "-A/--reboot-after"
   job option, the CLI tool has a feature that allows you to simply use:

   ::
      # arcli job -a -Ai ...

   If "i" uniquely distinguishes one of the RPC literals, it's going to be
   substituted by it. This allows less code duplication and quicker command
   entries.

 * A command line tool, currently named "arcli", that adds a thin layer on
   top of the API. It currently exposes actions such as listing, creating
   and deleting objects from Autotest RPC Server. Say, to add a new host:

   ::
      # arcli host -c -n newhost.mydomain.org

   And to list all the jobs:

   ::
      # arcli job -l

   To list only the currently running jobs:

   ::
      # arcli job -l --running

 * Portability: even though CPython itself is already portable, I want to
   give users no excuses for not running a test job. I've been testing arc,
   as in running the API examples and the "arcli" tool, on:

   - CPython 2.7
   - CPython 3.2
   - Jython 2.7
   - IronPython 2.7 via mono

   This has the immediate benefits of being able to distribute it and install
   either via Python package (publishing it in PyPi) or via distribution
   packages and target at the same time python 2.7 and python 3.x bases.

   On the dreamer side of things, I really wish this could open up the
   possibilities for things such as:
   - Writing plugins for other testing systems, such as Jenkins[3], using
     Java/Jython and arc.
   - Having a custom autotest client delivered via a Java Applet (or even
     Silverlight)
   - Custom autotest clients for mobile devices

 * As a proof of concept of portability, "arc" has been backed in a Java
   tarball, "arc.jar", and has all the features of arcli: 

   ::
       # java -jar arc.jar job -l
       ID    NAME
       1     sleep
       2     sleep
       3     sleep

   A bit more work and we could have a webstart based app.

 * API Documentation. Arc now makes use of Sphinx, the same documentation tool
   used by the Python project itself to generated nice documentation. The basic
   structured is already in-place, and you can take a look at the current docs
   by running say, "make html" at the docs" directory. The resulting docs will
   be under "build/html" for that specific output type.

 * The Plugin architecture is mostly in-place, and things such as command line
   arguments, actions and others are loaded transparently from Python modules
   at specific locations. This means that, to add a new command line action,
   one would have to write:

   arc/cli/args/myaction.py - for the command line arguments
   arc/cli/actions/myaction.py - for the action executing code


What's being worked on:
-----------------------
 * Comprehensive set of Unittests


[1] http://autotest.github.com
[2] https://github.com/autotest/virt-test
[3] http://jenkins-ci.org/
