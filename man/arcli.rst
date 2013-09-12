:title: arcli
:subtitle: Autotest RPC Client Application
:title_upper: ARCLI
:manual_section: 1

SYNOPSIS
========

.. include:: build/cli_usage.txt


DESCRIPTION
===========

`arcli` is the Autotest RPC client command line interface application. In a
nutshell, it allows users to interact with an Autotest server by means of
its RPC service.


OPTIONS
=======

The following list of options are global `arcli` options. Most options are
actually sub command options, as described in the SUB COMMANDS section::

 -h, --help           show this help message and exit
 --host HOST          Hostname or IP address for the autotest server


SUB COMMANDS
===========

`arcli` usage is broken into sub commands. This is the current list of sub commands:

* host
* job
* label
* test

Most sub commands accept common options, such as `-n | --name` and `-i | --id`.
So, suppose you're looking for a job with an specific ID, you'd use::

 $ arcli job -i <job_id> ...

Likewise, when looking for a host with a given name, you'd use::

 $ arcli host -n <host_name> ...


HOSTS SUB COMMAND
----------------

.. include:: build/cli_usage_host.txt


DESCRIPTION
~~~~~~~~~~~

The hosts command allow the user to manipulate hosts on an autotest server,
including adding new hosts and removing existing ones.

It's also possible to manage their temporary availability, which is known as
locking and unlocking machines.

If a given host is not in "Ready" state, you can also ask for a re-verification
job to be sent.

.. include:: build/cli_args_host.txt


ADDING A NEW HOST
~~~~~~~~~~~~~~~~~

To add a new host you just have to provide its name, which is usually the
hostname or the fully qualified host name::

    $ arcli host -a -n host.testgrid.example

The long form of the command would be::

    $ arcli host --add --name host.testgrid.example


REMOVING AN EXISTING HOST
~~~~~~~~~~~~~~~~~~~~~~~~~

To remove an existing host you can provide either its name or its numeric
identifier:

    $ arcli host -d -n host.testgrid.example
    $ arcli host -d -i 1

The long form of the command would be::

    $ arcli host --delete --name host.testgrid.example
    $ arcli host --delete --id 1


LISTING HOSTS
~~~~~~~~~~~~~

You can list the hosts registered on the server by using::

   $ arcli host -l

or::

   $ arcli host --list-brief


LISTING JOBS
~~~~~~~~~~~~

You can list the test jobs that are currently running on each host by using::

   $ arcli host -j

or::

   $ arcli host --list-jobs


LOCKING A HOST
~~~~~~~~~~~~~~

To lock a host and make it unavailable for the server to schedule new jobs on it, run::

    $ arcli host --lock -n host.fqdn.org

You could use a host numeric identifier::

    $ arcli host --lock -i 1


UNLOCKING A HOST
~~~~~~~~~~~~~~~~

To unlock a host and make it available for the server to schedule new jobs on it, run:

::

    $ arcli host --unlock -n host.fqdn.org


JOB SUB COMMAND
--------------

.. include:: build/cli_usage_job.txt


DESCRIPTION
~~~~~~~~~~~

The job command allows to create new jobs and list existing jobs.

.. include:: build/cli_args_job.txt


LABEL SUB COMMAND
----------------

.. include:: build/cli_usage_label.txt


DESCRIPTION
~~~~~~~~~~~

The label command allows to create new labels and list existing labels.

.. include:: build/cli_args_label.txt


TEST SUB COMMAND
---------------

.. include:: build/cli_usage_test.txt


DESCRIPTION
~~~~~~~~~~~

The test command allows to create new tests and list existing tests.

.. include:: build/cli_args_test.txt


FILES
=====

::

 /etc/arc.conf
    system wide configuration file

 ~/.arc.conf
    user specific configuration file


BUGS
====

If you find a bug, please report it over our github page as an issue.


AUTHOR
======

Cleber Rosa <cleber@redhat.com>
