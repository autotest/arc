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
Module that implements the actions for the CLI App when the linuxdistro
toplevel command is used
"""

import difflib

import arc.utils
import arc.linuxdistro
import arc.cli.actions.base


def format_distro(distro, label=None):
    '''
    Formats a LinuxDistro data in a suitable way to be displayed to a user

    :param distro: the :class:`arc.linuxdistro.LinuxDistro` to be printed
    :type distro: :class:`arc.linuxdistro.LinuxDistro`
    :param label: an optional label to add to the printed LinuxDistro title
    :type label: str
    :returns: formatted :class:`arc.linuxdistro.LinuxDistro`
    :rtype: str
    '''
    result = []

    if label is not None:
        result.append("Linux Distro %s" % label)

    result.append("\tname: %s" % distro.get("name", "unknown"))
    result.append("\tversion: %s" % distro.get("version", "unknown"))
    result.append("\trelease: %s" % distro.get("release", "unknown"))
    result.append("\tarch: %s" % distro.get("arch", "unknown"))

    return result

def print_distro(distro, label=None):
    '''
    Prints the given LinuxDistro

    :param distro: the :class:`arc.linuxdistro.LinuxDistro` to be printed
    :type distro: :class:`arc.linuxdistro.LinuxDistro`
    :param label: an optional label to add to the printed LinuxDistro title
    :type label: str
    :returns: None
    :rtype: None
    '''
    lines = format_distro(distro, label)
    lines = ["%s\n" % l for l in lines]
    print("".join(lines))


def print_diff(distro_1, distro_2):
    '''
    Prints the differences between two LinuxDistro

    :param distro_1: the first :class:`arc.linuxdistro.LinuxDistro`
    :type distro_1: :class:`arc.linuxdistro.LinuxDistro`
    :param distro_2: the second :class:`arc.linuxdistro.LinuxDistro`
    :type distro_2: :class:`arc.linuxdistro.LinuxDistro`
    :returns: None
    :rtype: None
    '''
    distro_1_id = distro_1.get("id")
    distro_1 = format_distro(distro_1)
    distro_1 = ["%s\n" % l for l in distro_1]

    distro_2_id = distro_2.get("id")
    distro_2 = format_distro(distro_2)
    distro_2 = ["%s\n" % l for l in distro_2]

    output = difflib.unified_diff(distro_1, distro_2,
                                  "Linux Distro #%s" % distro_1_id,
                                  "Linux Distro #%s" % distro_2_id)
    output = "".join(output)
    arc.utils.print_diff(output)


@arc.cli.actions.base.action
def show(app):
    linux_distro = arc.linuxdistro.get_data_by_id(app.connection,
                                                  app.parsed_arguments.id)
    if linux_distro is not None:
        print_distro(linux_distro)
    else:
        print('Linux Distro with id "%s" does not exist' %
              app.parsed_arguments.id)
        return -1


@arc.cli.actions.base.action
def diff(app):
    ids = arc.utils.parse_pair(app.parsed_arguments.pair)
    distro_1 = arc.linuxdistro.get_data_by_id(app.connection, ids[0])
    distro_2 = arc.linuxdistro.get_data_by_id(app.connection, ids[1])
    print_diff(distro_1, distro_2)
