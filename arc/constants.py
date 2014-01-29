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
This module holds a collection of data that should be treated as constants
because they should match what's defined as valid on autotest's rpc server

These constants come from autotest rpc server such as:
   frontend/afe/model_attributes.py
"""


__all__ = ['JOB_VALID_REBOOT_BEFORE',
           'JOB_VALID_REBOOT_AFTER',
           'TEST_VALID_TYPES']


#
# Thse constants control if machines should be rebooted before and after
# a given job is actually initiated
#
JOB_VALID_REBOOT_BEFORE = ('Never', 'If dirty', 'Always')
JOB_VALID_REBOOT_AFTER = ('Never', 'If all tests passed', 'Always')


#
# Autotest has two main types of tests
#
TEST_VALID_TYPES = ('Client', 'Server')


#
# Autotest jobs have different priorities
#
JOB_PRIORITIES = ('Low', 'Medium', 'High', 'Urgent')
