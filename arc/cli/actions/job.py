"""
Module that implements the actions for the CLI App when the job toplevel
command is used
"""


import functools

import arc.cli.actions.base
import arc.job
import arc.host


OBJ_NAME = "job"


_list_brief = functools.partial(arc.cli.actions.base.list_brief,
                                arc.job.get_objs)


def list_brief(app):
    """
    Lists briefly the jobs run and/or running on this server
    """
    return _list_brief(app, running=app.parsed_arguments.running)


def add(app):
    """
    Add (create) a new job
    """
    machines = app.parsed_arguments.machines
    hosts, meta_hosts = arc.host.parse_specification(app.connection, machines)

    result = arc.job.add_complete(
        connection=app.connection,
        name=app.parsed_arguments.name,
        priority=app.parsed_arguments.priority,
        control_file=app.parsed_arguments.control_file.read(),
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


delete = functools.partial(arc.cli.actions.base.delete_by_id,
                           OBJ_NAME, arc.job.Job, arc.job.delete)
