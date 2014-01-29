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
Module that implements the actions for the CLI App when the testenvironment
toplevel command is used
"""

import os
import sys
import difflib
import logging

import arc.utils
import arc.testenvironment
import arc.cli.actions.base
import arc.cli.actions.linuxdistro

def format_kind_default(software_component):
    return ('%(kind)s %(name)s (version: %(version)s, '
            'release: %(release)s, arch: %(arch)s, '
            'checksum: %(checksum)s)' % software_component)

def format_kind_git_repo(software_component):
    return ('%(kind)s %(name)s (commit: %(checksum)s)' % software_component)

formatters = {"default": format_kind_default,
              "git_repo": format_kind_git_repo}

def format_software_components(software_components):
    result = []
    for sc in software_components:
        formatter = formatters.get(sc.get("kind", "default"),
                                   format_kind_default)
        result.append(formatter(sc))
    return result

def print_software_components(software_components):
    lines = format_software_components(software_components)
    lines = ["%s\n" % l for l in lines]
    print("".join(lines))

@arc.cli.actions.base.action
def show(app):

    test_environment = app.parsed_arguments.show
    test_env_list = arc.testenvironment.get_data(app.connection,
                                                 pk=test_environment)
    if len(test_env_list) != 1:
        print("Failed to fetch data for the requested Test Environment")
        return -1

    test_env = test_env_list[0]
    label = 'for test environment #%s:' % test_environment


    software_components = app.connection.run(
        'afe',
        'get_test_environment_installed_software_components',
        test_environment)

    arc.cli.actions.linuxdistro.print_distro(test_env['distro'], label)
    print_software_components(software_components)


def get_diff(connection, ids):
    te_1 = arc.testenvironment.get_data(connection, pk=ids[0])[0]
    te_1_distro_id = te_1["distro"]["id"]
    te_2 = arc.testenvironment.get_data(connection, pk=ids[1])[0]
    te_2_distro_id = te_2["distro"]["id"]

    if te_1_distro_id != te_2_distro_id:
        distro_1 = arc.linuxdistro.get_data_by_id(connection,
                                                  te_1_distro_id)
        distro_2 = arc.linuxdistro.get_data_by_id(connection,
                                                  te_2_distro_id)
        arc.cli.actions.linuxdistro.print_diff(distro_1, distro_2)
    else:
        logging.debug("Distros on compared test environments are the same")

    sc_1 = connection.run(
        'afe',
        'get_test_environment_installed_software_components',
        ids[0])
    sc_1 = format_software_components(sc_1)
    sc_1 = ["%s\n" % l for l in sc_1]

    sc_2 = connection.run(
        'afe',
        'get_test_environment_installed_software_components',
        ids[1])
    sc_2 = format_software_components(sc_2)
    sc_2 = ["%s\n" % l for l in sc_2]

    label = "Software Installed on Test Environment #%s"
    label_1 = label % ids[0]
    label_2 = label % ids[1]
    output = difflib.unified_diff(sc_1, sc_2, label_1, label_2)

    output = "".join(output)
    return output

@arc.cli.actions.base.action
def diff(app):
    output = get_diff(app.connection,
                      arc.utils.parse_pair(app.parsed_arguments.diff))

    arc.utils.print_diff(output)
