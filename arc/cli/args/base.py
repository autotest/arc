"""
This module has base action arguments that are used on other top level commands

These top level commands import these definitions for uniformity and
consistency sake
"""

__all__ = ['ADD', 'LIST_BRIEF', 'DELETE']


ADD = (('-a', '--add',),
       {'help': 'add a new entry',
        'action': 'store_true',
        'default': False})


LIST_BRIEF = (('-l', '--list-brief',),
              {'help': 'list all records briefly',
               'action': 'store_true',
               'default': False})


DELETE = (('-d', '--delete',),
          {'help': 'delete an existing entry',
           'action': 'store_true',
           'default': False})
