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
