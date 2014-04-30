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
Module that implements the actions for the CLI App when the test toplevel
command is used
"""
import sys

import arc.utils
import arc.tko.test
import arc.cli.actions.base
import arc.cli.actions.testenvironment


@arc.cli.actions.base.action
def find(app):

    test = app.parsed_arguments.name
    error = arc.tko.test.get_data(app.connection, test=test, status=3)
    failure = arc.tko.test.get_data(app.connection, test=test, status=4)
    success = arc.tko.test.get_data(app.connection, test=test, status=5)

    has_error = len(error) > 0
    has_failure = len(failure) > 0
    has_success = len(success) > 0

    if not (has_success and (has_error or has_failure)):

        if has_success and not (has_error or has_failure):
            print('Only success has been found for the given test')

        if (has_error or has_failure) and not has_success:
            print('Only failure has been found for the given test')

        print('Insufficient data to determine a regression point')
        sys.exit(-1)

    # sorts by job_idx the latest job error/failure
    last_failure_test = -1
    last_failure_job = -1
    last_failure_test_env = -1
    for i in error:
        if i['test_idx'] > last_failure_test:
            last_failure_test = i['test_idx']
            last_failure_job = i['job']
            last_failure_test_env = i['test_environment']

    for i in failure:
        if i['test_idx'] > last_failure_test:
            last_failure_test = i['test_idx']
            last_failure_job = i['job']
            last_failure_test_env = i['test_environment']

    last_success_test = -1
    last_success_job = -1
    last_success_test_env = -1
    for i in success:
        if i['test_idx'] > last_success_test:
            last_success_test = i['test_idx']
            last_success_job = i['job']
            last_success_test_env = i['test_environment']

    print('Last success reported in test: %s (job %s)' % (last_success_test,
                                                          last_success_job))

    print('Last failure reported in test: %s (job %s)' % (last_failure_test,
                                                          last_failure_job))

    if last_success_test_env == last_failure_test_env:
        print('There was no perceived change in the test environment')
        sys.exit(0)

    output = arc.cli.actions.testenvironment.get_diff(app.connection,
                                                      [last_success_test_env,
                                                       last_failure_test_env])
    arc.utils.print_diff(output)
