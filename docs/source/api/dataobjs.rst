.. _arc-dataobjs:

Manipulating Data and Objects
=============================

A big part of Arc is to allow easy and conviente access to the data about Jobs, Tests, Hosts and others on an Autotest RPC Server.

Base functions
--------------

Autotest RPC communication between client and server is based on the JSON RPC protocol. Because the protocol itself has no builtin tooling for creating stubs and skeletons, Arc makes use of some programming techiniques to compensate for that.

First, a series of functions that allow one to fetch, create, modify and delete data on the server (such as jobs and tests records) are created by specializing functions.

The :mod:`arc.base` module contains functions that are used py the Standard Python Library module :mod:`functools` to create versions of functions that operate on Jobs, Tests, Hosts, Labels, etc.

.. automodule:: arc.base
   :members:


Manipulating raw JSON data
--------------------------

The following functions manipulate JSON data directly. Some of these functions
allow you to:

 * fetch only a subset of records
 * filter only some fields out of the returned records

But that is all the data massaging that will be done by their behalf.

.. function:: get_data_by_id(identification)

   Get remote object data by its ID.


Manipulating objects
--------------------

These methods return objects that wrap the data returned by the server.

.. function:: get_objs

This function will return Host objects. By default, it will return object for all currently active Hosts on the Autotest RPC server, but it's possible to specify a custom search filter through the :param data_filter.

|generator|


Data and Object Modules
-----------------------

.. toctree::
   :maxdepth: 2

   host
   job
   label

.. include:: defs.txt
