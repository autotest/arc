#!/usr/bin/python
#
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

import os
import sys
import StringIO

THIS_FILE = os.path.abspath(__file__)
MAN_DIR = os.path.dirname(THIS_FILE)
BUILD_DIR = os.path.join(MAN_DIR, 'build')
ARC_DIR = os.path.dirname(MAN_DIR)

sys.path.insert(0, ARC_DIR)

import arc.cli.args.parser


class DummyParser(arc.cli.args.parser.Parser):
    def exit(self):
        pass


def process_usage(usage):
    if usage.startswith('usage: '):
        rest = usage[8:]
    else:
        rest = usage

    rest_parts = rest.split(' ')
    rest_parts[0] = 'arcli'
    rest = ' '.join(rest_parts)
    return rest


def parser_to_rest():
    p = arc.cli.args.parser.Parser()
    p.add_arguments_on_all_modules()
    usage = p.format_usage()
    rest = process_usage(usage)
    return rest


def process_subcommand_usage(usage):
    result = []
    result.append('::')
    result.append('')
    for line in usage:
        if line == '\n':
            break

        line = line.strip()
        if line.startswith('usage: '):
            result.append(' %s' % line[7:])
        else:
            result.append(' %s' % line)
    result.append('')

    return '\n'.join(result)


def parser_subcommand_to_rest(command):
    p = DummyParser()
    p.add_arguments_on_all_modules()

    original_stdout = sys.stdout
    sys.stdout = StringIO.StringIO()

    try:
        p.parse_args([command, '--help'])
    except SystemExit:
        pass

    usage = sys.stdout
    sys.stdout = original_stdout

    usage.seek(0)
    usage = usage.readlines()
    rest = process_subcommand_usage(usage)
    return rest


def parser_to_rest_build_file(command=None):
    if not os.path.isdir(BUILD_DIR):
        os.mkdir(BUILD_DIR)

    if command is None:
        output_file_name = 'cli_usage.txt'
    else:
        output_file_name = 'cli_usage_%s.txt' % command

    output_file_path = os.path.join(BUILD_DIR,
                                    output_file_name)

    output = open(output_file_path, 'w')
    if command is None:
        output.write(parser_to_rest())
    else:
        output.write(parser_subcommand_to_rest(command))
    output.close()

if __name__ == '__main__':
    parser_to_rest_build_file()
