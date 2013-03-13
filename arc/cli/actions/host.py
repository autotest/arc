"""
Module that implements the actions for the CLI App when the host toplevel
command is used
"""


import functools

import arc.cli.actions.base
import arc.host
import arc.defaults


OBJ_NAME = "host"


list_brief = functools.partial(arc.cli.actions.base.list_brief,
                               arc.host.get_objs)


add = functools.partial(arc.cli.actions.base.add_with_name,
                        OBJ_NAME, arc.host.add)


delete = functools.partial(arc.cli.actions.base.delete,
                           OBJ_NAME, arc.host.Host, arc.host.delete)


def list_jobs(app):
    """
    List host and jobs currently running on them

    :param app: the running application instance
    """
    def get_job_id_name(queue, host_id):
        for j in queue:
            if j['host']['id'] == host_id:
                return (j['job']['id'], j['job']['name'])
        return ('', '')

    line_fmt = "%-6s%-34s%-8s%-80s"
    header = line_fmt % ("ID", "NAME", "JOB ID", "JOB NAME")
    header_printed = False
    queue = app.connection.run(arc.defaults.AFE_SERVICE_NAME,
                               'get_host_queue_entries', active=True)
    hosts = arc.host.get_objs(app.connection)
    for h in hosts:
        if not header_printed:
            print(header)
            header_printed = True

        (job_id, job_name) = get_job_id_name(queue, h.identification)

        print(line_fmt % (h.identification,
                          h.name,
                          job_id,
                          job_name))


def lock(app):
    '''
    Locks the chosen host

    :param app: the running application instance
    '''
    if app.parsed_arguments.name:
        arc.host.modify(app.connection,
                        app.parsed_arguments.name,
                        locked=True)


def unlock(app):
    '''
    Unlocks the chosen host

    :param app: the running application instance
    '''
    if app.parsed_arguments.name:
        arc.host.modify(app.connection,
                        app.parsed_arguments.name,
                        locked=False)


def reverify(app):
    '''
    Schedules a reverification for the chosen host

    :param app: the running application instance
    '''
    if app.parsed_arguments.name:
        arc.host.reverify(app.connection,
                          app.parsed_arguments.name)
