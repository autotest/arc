.. _about-arc:

About Arc
=========

Arc is the Autotest_ RPC Client, both a library and a command line tool to
interact with an Autotest_ Server through its RPC services.

There's no way to really understand the purpose of Arc without a brief
understanding of what Autotest_ is and how it operates.

.. _about-autotest:

About Autotest
--------------

Autotest_ is a fully automated framework for testing, that is used to test, among other pieces of software, the Linux kernel.

Autotest_ can run tests in two modes:

1. "autotest-local", also known as "client mode"

   In this mode, a test runs on the same machine where "autotest-local" was executed. The basic autotest libraries are used, as the "autotest-local" test runner itself. The other pieces of running code are the test itself.

2. "autotest-remote", also known as "server mode"

   In this mode, the machine where "autotest-remote" was run connects to another machine, sets up an "autotest client" environment, including copying it's own copy of the autotest client framework to the client machine, and then starting the test by means of "autotest-local".

Running "autotest-remote" manually with lots of parameters is usually not the most convenient thing to do, so Autotest_ also provides a server that does scheduling of test jobs. Arc, the Autotest_ RPC Client, is a piece of software that communicates with the Autotest_ RPC server.

Arc allows you to view and modify the server side objects, such as the machines (hosts in Autotest_ terminology) that will eventually run the tests, jobs that have already run or are currently running, the tests that are registered on the server, etc.

.. _Autotest: http://autotest.github.io
