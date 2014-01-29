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
Module that implements the actions for the CLI App when the job toplevel
command is used
"""


import functools
import os
import shutil
import tempfile

import arc.cli.actions.base
import arc.job
import arc.tko.job
import arc.host
import arc.test


OBJ_NAME = "job"


_list_brief = functools.partial(arc.cli.actions.base.list_brief,
                                arc.job.get_objs)


@arc.cli.actions.base.action
def list_brief(app):
    """
    Lists briefly the jobs run and/or running on this server
    """
    running = not app.parsed_arguments.all
    return _list_brief(app, running=running)


@arc.cli.actions.base.action
def add(app):
    """
    Add (create) a new job
    """
    machines = app.parsed_arguments.machines
    hosts, meta_hosts = arc.host.parse_specification(app.connection, machines)

    if app.parsed_arguments.from_test_number:
        content = arc.test.get_control_file_by_id(app.connection,
                                                  app.parsed_arguments.from_test_number)
        control_file = open(create_control_file(content))

    if app.parsed_arguments.control_file:
        control_file = app.parsed_arguments.control_file

    # Open the Control File in vi or $EDITOR
    if app.parsed_arguments.edit_before_sending is True:
        control_file = edit_control_file(control_file)

    result = arc.job.add_complete(
        connection=app.connection,
        name=app.parsed_arguments.name,
        priority=app.parsed_arguments.priority,
        control_file=control_file.read(),
        control_type=app.parsed_arguments.test_type,
        hosts=hosts,
        profiles=app.parsed_arguments.profiles,
        # FIXME: for now we only use the machines params
        meta_hosts=meta_hosts,
        one_time_hosts=(),
        atomic_group_name=None,
        synch_count=None,
        is_template=False,
        timeout=None,
        max_runtime_hrs=None,
        run_verify=True,
        email_list='',
        dependencies=(),
        reboot_before=app.parsed_arguments.reboot_before,
        reboot_after=app.parsed_arguments.reboot_after,
        parse_failed_repair=None,
        hostless=False,
        keyvals=None,
        drone_set=None)
    app.log.info("Job creation: %s", result)


delete = arc.cli.actions.base.action(
    functools.partial(arc.cli.actions.base.delete_by_id,
                      OBJ_NAME, arc.job.Job, arc.job.delete))

def edit_control_file(control_file):
    editor = os.environ.get('EDITOR', 'vi')
    fd, new_control_file = tempfile.mkstemp(prefix='control')
    shutil.copyfile(control_file.name, new_control_file)
    os.system(editor + ' ' + new_control_file)
    control_file = open(new_control_file)
    return control_file

def create_control_file(content):
    fd, new_control_file = tempfile.mkstemp(prefix='control')
    with open(new_control_file, 'w') as f:
        f.write(content)
    return new_control_file

def print_job(connection, job_id, show_all=False):
    job = arc.job.get_data_by_id(connection, job_id)

    job_labels = {}
    for k in job.keys():
        label = k.replace("_", " ")
        words = label.split(" ")
        words = [w.capitalize() for w in words]
        label = " ".join(words)
        job_labels[k] = label


    if not show_all:
        skip = ["control_file", "parameterized_job", "reserve_hosts",
                "keyvals", "drone_set", "run_verify", "control_type",
                "reboot_before", "max_runtime_hrs", "priority",
                "parse_failed_repair", "dependencies", "timeout",
                "synch_count", "reboot_after"]
        for label in skip:
            del(job_labels[label])

    order = ["id", "name", "owner", "email_list", "created_on"]
    for label in order:
        print("%s: %s" % (job_labels[label],
                          job[label]))
        del(job_labels[label])
    print("")

    for label in job_labels:
        # always skip the control_file contents
        if label == "control_file":
            continue
        print("%s: %s" % (job_labels[label],
                          job[label]))

    # finally, print the control
    if show_all:
        print("Control File Contents:")
        print("===================== CONTROL FILE START =====================")
        print("%s" % job["control_file"])
        print("====================== CONTROL FILE END ======================")


@arc.cli.actions.base.action
def show(app):
    print_job(app.connection,
              app.parsed_arguments.show,
              app.parsed_arguments.all)
