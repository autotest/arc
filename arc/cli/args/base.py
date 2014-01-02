"""
This module has base action arguments that are used on other top level commands

These top level commands import these definitions for uniformity and
consistency sake
"""

__all__ = ['ADD', 'LIST_BRIEF', 'LIST_FULL', 'DELETE', 'NAME', 'ID']


#
# Arguments that are treated as actions
#
ADD = (('-a', '--add',),
       {'help': 'add a new entry',
        'action': 'store_true',
        'default': False})


LIST_BRIEF = (('-l', '--list-brief',),
              {'help': 'list all records briefly',
               'action': 'store_true',
               'default': False})


LIST_FULL = (('-ll', '--list-full',),
             {'help': 'list all records with all information',
              'action': 'store_true',
               'default': False})


DELETE = (('-d', '--delete',),
          {'help': 'delete an existing object',
           'action': 'store_true',
           'default': False})


#
# Other arguments that will influence action behaviour
#
NAME = (('-n', '--name'),
        {'help': 'name of the object'})


ID = (('-i', '--id'),
      {'help': 'numeric identification of the object',
       'type': int})
