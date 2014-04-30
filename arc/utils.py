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

'''
Top level collection of utility functions, that is, avaible to to be used by
any part of the library or directly by applications.
'''

import os
import sys

try:
    import pygments
    import pygments.lexers
    import pygments.formatters
    PYGMENTS_AVAILABLE = True
except ImportError:
    PYGMENTS_AVAILABLE = False


def parse_pair(pair):
    '''
    Parse a string that expresses a pair of integers

    :param pair: an expression for two integers
    :type pair: str
    :returns: a pair of integers
    :rtype: list
    '''
    for separator in ("..", ","):
        if separator in pair:
            ids = pair.split(separator)
            if ids[-1] == "":
                ids = ids[:-1]

            if len(ids) > 1:
                ids = [int(ids[0]), int(ids[1])]
                break
            else:
                # note: pair should be last id on database, not -1. since this
                # require quite a few roundtrips to the database, and makes
                # and is really specific to the "type" of ID we're dealing
                # with and also the fact that this code is used during the app
                # argument parsing, let's assume -1 for now
                ids = [int(ids[0]), int(ids[0]) - 1]
                break
    return ids


def print_diff(output):
    '''
    Prints a diff output to the standard output, optionally using

    :param output: the diff text to be printed out
    :type output: str
    :returns: None
    :rtype: None
    '''
    if os.isatty(sys.stdout.fileno()) and PYGMENTS_AVAILABLE:
        output = pygments.highlight(
            output,
            pygments.lexers.get_lexer_by_name('diff'),
            pygments.formatters.get_formatter_by_name('terminal'))
    print(output)


def print_tabular_data(fields, values, show_header=True):
    '''
    Prints a tabular data to the standard output.
    :param fields: list of field names
    :param values: list of values (same size as fields)
    :param show_header: should print header?
    :rtype: None
    '''
    sizes = [len(x) for x in fields]
    for value in values:
        value = [len(str(x)) for x in value]
        sizes = [max(x, y) for x, y in zip(sizes, value)]
    mask = ['{:<%d}' % x for x in sizes]
    mask = ' '.join(mask)
    if show_header is True:
        print mask.format(*fields)
    for value in values:
        print mask.format(*value)


def print_objs_brief_as_table(objs):
    '''
    Prints objects as a table (brief).
    :param objs: the objects...
    :rtype: None
    '''
    values = []
    for obj in objs:
        values.append((str(obj.identification), obj.name))
    if values:
        fields = [obj.ID_FIELD.upper(), obj.NAME_FIELD.upper()]
        print_tabular_data(fields, values)


def print_objs_as_table(objs):
    '''
    Prints objects as a table (full).
    :param objs: the objects...
    :rtype: None
    '''
    values = []
    for obj in objs:
        val = [str(obj.identification), obj.name]
        for fld in obj.FIELDS:
            val.append(getattr(obj, fld, ''))
        values.append(val)
    if values:
        fields = [obj.ID_FIELD.upper(), obj.NAME_FIELD.upper()]
        extra = [x.upper() for x in obj.FIELDS]
        fields.extend(extra)
        print_tabular_data(fields, values)


def print_obj_content(obj):
    '''
    Prints object content.
    :param obj: the object
    :rtype: None
    '''
    for fld in obj.keys():
        label = fld.replace('_', ' ').title()  # 'foo_bar' => 'Foo Bar'
        print "%s: %s" % (label, obj[fld])
