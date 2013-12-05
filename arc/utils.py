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
                ids = [int(ids[0]), int(ids[0])-1]
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
